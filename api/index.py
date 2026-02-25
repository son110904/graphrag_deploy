"""
api/index.py — NEU Graph Agent (Vercel Serverless)
Tích hợp đầy đủ logic từ script3.py:
  - Intent detection (keywords, mentioned_labels, asked_label, negated_keywords, is_comparison)
  - Relationship constraints per query type
  - Targeted Cypher queries theo intent
  - Community Detection filter
  - Multi-hop BFS traversal
  - PageRank ranking + negation filter
  - Seed entity injection
  - LLM generate_answer với đầy đủ prompt + constraints

Tối ưu cho Vercel (giới hạn 10s):
  - Giảm LIMIT traversal
  - Dùng targeted query trước BFS
  - Neo4j connection reuse qua module-level driver
"""

import os
import json
import uuid
import datetime
from neo4j import GraphDatabase
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────────────────────────────
NEO4J_URI      = os.getenv("DB_URL")
NEO4J_USERNAME = os.getenv("DB_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("DB_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

MAX_HOPS = int(os.getenv("MAX_HOPS", "2"))   # Giảm xuống 2 cho Vercel timeout
TOP_K    = int(os.getenv("TOP_K", "5"))
# ──────────────────────────────────────────────────────────────────────────────

# Module-level clients (reuse giữa các invocations trên cùng instance)
ai_client = OpenAI(api_key=OPENAI_API_KEY)
driver    = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── CONSTANTS ────────────────────────────────────────────────────────────────

NEGATION_SYNONYMS = {
    "ko", "k", "không", "chẳng", "chả", "kém", "chưa giỏi",
    "không giỏi", "ko giỏi", "k giỏi", "yếu", "dở",
    "không thích", "ko thích", "k thích", "chán",
    "không muốn", "ko muốn", "không có", "ko có",
    "không biết", "ko biết", "chưa biết",
}

SCHEMA_DESC = """
Nodes: MAJOR{name,code,community_id,pagerank}, SUBJECT{name,code,community_id,pagerank},
       SKILL{name,community_id,pagerank}, CAREER{name,community_id,pagerank},
       TEACHER{name,community_id}, DOCUMENT{name,docid,doctype}
Relationships:
  (MAJOR)-[:OFFERS]->(SUBJECT)
  (TEACHER)-[:TEACH]->(SUBJECT)
  (SUBJECT)-[:PROVIDES]->(SKILL)
  (CAREER)-[:REQUIRES]->(SKILL)
  (SUBJECT)-[:PREREQUISITE_FOR]->(SUBJECT)
  (MAJOR)-[:LEADS_TO]->(CAREER)
  (*)-[:MENTIONED_IN]->(DOCUMENT)
All name values are UPPERCASE Vietnamese.
"""

RELATIONSHIP_CONSTRAINTS = {
    ("MAJOR", "CAREER"): (
        "Đường truy xuất: MAJOR -[:LEADS_TO]-> CAREER.\n"
        "Chỉ liệt kê các nghề nghiệp (CAREER) mà ngành (MAJOR) dẫn đến.\n"
        "KHÔNG đề cập SUBJECT (môn học) trừ khi được hỏi thêm."
    ),
    ("CAREER", "SKILL"): (
        "Đường truy xuất: CAREER -[:REQUIRES]-> SKILL và SUBJECT -[:PROVIDES]-> SKILL.\n"
        "Trả lời: kỹ năng cần thiết cho nghề đó + môn học cung cấp kỹ năng tương ứng.\n"
        "Kèm mã môn học nếu có."
    ),
    ("MAJOR", "SKILL"): (
        "Đường truy xuất: MAJOR -[:OFFERS]-> SUBJECT -[:PROVIDES]-> SKILL.\n"
        "Trả lời: kỹ năng đạt được từ các môn học trong chương trình đào tạo.\n"
        "Kèm tên môn học (mã môn) cung cấp kỹ năng đó."
    ),
    ("SKILL", "MAJOR"): (
        "Đường truy xuất: SKILL <-[:PROVIDES]- SUBJECT <-[:OFFERS]- MAJOR.\n"
        "Trả lời: ngành học (MAJOR) có môn học cung cấp kỹ năng đó.\n"
        "Kèm mã ngành, tên môn trung gian."
    ),
    ("CAREER", "SUBJECT"): (
        "Đường truy xuất: CAREER -[:REQUIRES]-> SKILL <-[:PROVIDES]- SUBJECT.\n"
        "Trả lời: các môn học cung cấp kỹ năng mà nghề đó yêu cầu.\n"
        "Kèm mã môn học và kỹ năng tương ứng."
    ),
    ("MAJOR", "SUBJECT"): (
        "Đường truy xuất: MAJOR -[:OFFERS]-> SUBJECT.\n"
        "Trả lời: các môn học thuộc chương trình ngành đó, kèm mã môn và kỹ năng cung cấp (SKILL)."
    ),
    ("SKILL", "CAREER"): (
        "Đường truy xuất: SKILL <-[:REQUIRES]- CAREER.\n"
        "Trả lời: danh sách nghề nghiệp yêu cầu kỹ năng đó."
    ),
    ("CAREER", "MAJOR"): (
        "Đường truy xuất: MAJOR -[:LEADS_TO]-> CAREER.\n"
        "Trả lời: ngành học (MAJOR) dẫn đến nghề đó, kèm mã ngành."
    ),
    ("SUBJECT", "SKILL"): (
        "Đường truy xuất: SUBJECT -[:PROVIDES]-> SKILL.\n"
        "Trả lời: kỹ năng đạt được sau khi học môn đó."
    ),
    ("SKILL", "SUBJECT"): (
        "Đường truy xuất: SKILL <-[:PROVIDES]- SUBJECT.\n"
        "Trả lời: môn học (kèm mã môn) cung cấp kỹ năng đó, và ngành nào chứa môn đó."
    ),
    ("MAJOR", "MAJOR"): (
        "Đây là câu so sánh giữa các ngành.\n"
        "Truy xuất: MAJOR -[:LEADS_TO]-> CAREER và MAJOR -[:OFFERS]-> SUBJECT.\n"
        "Trả lời: so sánh cơ hội nghề nghiệp và môn học đặc trưng của từng ngành.\n"
        "Kèm mã ngành, mã môn học nếu có. Trích dẫn nguồn tài liệu (DOCUMENT) nếu có."
    ),
    ("MAJOR", "MAJOR_CAREER"): (
        "Đường truy xuất: MAJOR -[:LEADS_TO]-> CAREER và MAJOR -[:OFFERS]-> SUBJECT -[:PROVIDES]-> SKILL.\n"
        "Trả lời nghề nghiệp + kỹ năng đặc trưng + môn học trong ngành đó."
    ),
}

ANSWER_SYSTEM_BASE = """Bạn là trợ lý tư vấn học thuật cho Đại học Kinh tế Quốc dân (NEU).
Tổng hợp câu trả lời rõ ràng, tự nhiên bằng tiếng Việt từ kết quả Knowledge Graph đã xếp hạng.

{schema}

QUY TẮC QUAN TRỌNG:
1. Trả lời ĐÚNG TRỌNG TÂM câu hỏi. Không thêm thông tin không được hỏi đến.
2. Không dùng câu "ngoài ra..." để mở rộng ngoài phạm vi câu hỏi.
3. Nếu dữ liệu không đủ để trả lời → nói rõ "Dữ liệu hiện tại chưa đủ để tư vấn về [chủ đề], bạn có thể liên hệ phòng đào tạo để biết thêm."
4. KHÔNG bịa thông tin không có trong Knowledge Graph.
5. Luôn kèm mã ngành (MAJOR.code) và mã môn học (SUBJECT.code) khi có trong dữ liệu.
6. Khi người dùng đề cập thực thể mà họ KHÔNG giỏi / không thích → loại bỏ thực thể đó khỏi câu trả lời.
7. Ngôn ngữ tự nhiên, thân thiện — KHÔNG máy móc, lý thuyết.

RÀNG BUỘC THEO LOẠI CÂU HỎI:
{constraint}
"""

# ─── TARGETED QUERIES ─────────────────────────────────────────────────────────

TARGETED_QUERIES: dict[tuple[str, str], str] = {
    ("MAJOR", "CAREER"): """
        MATCH (start:MAJOR)-[:LEADS_TO]->(n:CAREER)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['LEADS_TO'] AS rel_types, [start.name, n.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
    ("CAREER", "SKILL"): """
        MATCH (start:CAREER)-[:REQUIRES]->(n:SKILL)
        WHERE toLower(start.name) CONTAINS toLower($kw)
           OR toLower(start.name) CONTAINS 'phân tích'
           OR toLower(start.name) CONTAINS 'analyst'
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['REQUIRES'] AS rel_types, [start.name, n.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
    ("MAJOR", "SKILL"): """
        MATCH (start:MAJOR)-[:OFFERS]->(sub:SUBJECT)-[:PROVIDES]->(n:SKILL)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['OFFERS','PROVIDES'] AS rel_types, [start.name, sub.name, n.name] AS node_names, 2 AS hops
        LIMIT 30
    """,
    ("SKILL", "MAJOR"): """
        MATCH (n:MAJOR)-[:OFFERS]->(sub:SUBJECT)-[:PROVIDES]->(start:SKILL)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['OFFERS','PROVIDES'] AS rel_types, [n.name, sub.name, start.name] AS node_names, 2 AS hops
        LIMIT 30
    """,
    ("SKILL", "CAREER"): """
        MATCH (n:CAREER)-[:REQUIRES]->(start:SKILL)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['REQUIRES'] AS rel_types, [n.name, start.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
    ("CAREER", "SUBJECT"): """
        MATCH (start:CAREER)-[:REQUIRES]->(sk:SKILL)<-[:PROVIDES]-(n:SUBJECT)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['REQUIRES','PROVIDES'] AS rel_types, [start.name, sk.name, n.name] AS node_names, 2 AS hops
        LIMIT 30
    """,
    ("MAJOR", "SUBJECT"): """
        MATCH (start:MAJOR)-[:OFFERS]->(n:SUBJECT)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['OFFERS'] AS rel_types, [start.name, n.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
    ("SKILL", "SUBJECT"): """
        MATCH (n:SUBJECT)-[:PROVIDES]->(start:SKILL)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['PROVIDES'] AS rel_types, [n.name, start.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
    ("SUBJECT", "SKILL"): """
        MATCH (start:SUBJECT)-[:PROVIDES]->(n:SKILL)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['PROVIDES'] AS rel_types, [start.name, n.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
    ("CAREER", "MAJOR"): """
        MATCH (n:MAJOR)-[:LEADS_TO]->(start:CAREER)
        WHERE toLower(start.name) CONTAINS toLower($kw)
        RETURN n.name AS name, labels(n)[0] AS label, n.code AS code,
               n.pagerank AS pagerank, n.community_id AS community_id,
               ['LEADS_TO'] AS rel_types, [n.name, start.name] AS node_names, 1 AS hops
        LIMIT 30
    """,
}


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 1: EXTRACT QUERY INTENT
# ══════════════════════════════════════════════════════════════════════════════

def extract_query_intent(question: str) -> dict:
    system_msg = (
        "Bạn phân tích câu hỏi tư vấn học thuật và trả về JSON.\n"
        "Schema Knowledge Graph:\n"
        "  Node labels: MAJOR (ngành học), SUBJECT (môn học), SKILL (kỹ năng), "
        "CAREER (nghề nghiệp / vị trí việc làm), TEACHER (giảng viên)\n\n"
        "Từ đồng nghĩa phủ định: ko, k, không, chẳng, kém, yếu, dở, chưa giỏi, "
        "không giỏi, không thích, không muốn, không biết\n\n"
        "PHÂN BIỆT QUAN TRỌNG:\n"
        "  - Hỏi 'môn học / môn nào / học môn gì' → asked_label: 'SUBJECT'\n"
        "  - Hỏi 'ngành nào / học ngành gì / chuyên ngành' → asked_label: 'MAJOR'\n"
        "QUAN TRỌNG - Chuẩn hóa keyword về tiếng Việt theo graph:\n"
        "  data analyst → chuyên viên phân tích dữ liệu\n"
        "  software engineer / developer → lập trình viên, kỹ sư phần mềm\n"
        "  tester / QA → kiểm thử\n"
        "  IT / information technology → công nghệ thông tin\n"
        "  AI / machine learning → trí tuệ nhân tạo, học máy\n"
        "  Nếu không biết tên tiếng Việt → giữ nguyên tiếng Anh\n\n"
        "Trả về JSON với đúng các trường sau:\n"
        "{\n"
        '  "keywords": ["từ khoá thực thể để tìm trong KG"],\n'
        '  "mentioned_labels": ["MAJOR|SUBJECT|SKILL|CAREER|TEACHER"],\n'
        '  "asked_label": "MAJOR|SUBJECT|SKILL|CAREER|TEACHER|UNKNOWN",\n'
        '  "negated_keywords": ["thực thể / kỹ năng / môn bị phủ định"],\n'
        '  "is_comparison": true\n'
        "}\n\n"
        "Ví dụ:\n"
        '  Câu: "Giỏi giao tiếp thì học ngành nào?" → mentioned_labels: ["SKILL"], asked_label: "MAJOR"\n'
        '  Câu: "Ngành CNTT có những nghề gì?" → mentioned_labels: ["MAJOR"], asked_label: "CAREER"\n'
        '  Câu: "Ko giỏi toán thì theo nghề lập trình viên được không?" '
        '→ negated_keywords: ["toán"], mentioned_labels: ["CAREER"]\n'
        '  Câu: "CNTT hay KTPM phù hợp hơn?" → is_comparison: true, mentioned_labels: ["MAJOR"]\n'
        '  Câu: "Học môn gì để làm lập trình viên?" → mentioned_labels: ["CAREER"], asked_label: "SUBJECT"\n'
        '  Câu: "Môn nào giúp tôi trở thành data analyst?" → mentioned_labels: ["CAREER"], asked_label: "SUBJECT"\n'
        '  Câu: "Cần học những môn gì cho nghề kế toán?" → mentioned_labels: ["CAREER"], asked_label: "SUBJECT"\n'
    )
    response = ai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user",   "content": f"Phan tich cau hoi sau va tra ve json: {question}"},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    parsed = json.loads(response.choices[0].message.content)
    return {
        "keywords":         parsed.get("keywords", []),
        "mentioned_labels": parsed.get("mentioned_labels", []),
        "asked_label":      parsed.get("asked_label", "UNKNOWN"),
        "negated_keywords": parsed.get("negated_keywords", []),
        "is_comparison":    parsed.get("is_comparison", False),
    }


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 2: FETCH SEED ENTITIES
# ══════════════════════════════════════════════════════════════════════════════

def fetch_seed_entities(keywords: list[str], mentioned_labels: list[str]) -> list[dict]:
    if not keywords or not mentioned_labels:
        return []
    label_filter = " OR ".join([f"n:{lbl}" for lbl in mentioned_labels])
    results = []
    with driver.session() as session:
        for kw in keywords:
            rows = session.run(f"""
                MATCH (n)
                WHERE ({label_filter})
                  AND toLower(n.name) CONTAINS toLower($kw)
                RETURN n.name AS name, labels(n)[0] AS label,
                       n.code AS code, n.pagerank AS pagerank,
                       n.community_id AS community_id
                LIMIT 3
            """, kw=kw).data()
            for r in rows:
                results.append({
                    "name": r["name"], "label": r["label"],
                    "code": r["code"], "pagerank": r["pagerank"],
                    "community_id": r["community_id"], "hops": 0,
                })
    return results


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 3: COMMUNITY DETECTION FILTER
# ══════════════════════════════════════════════════════════════════════════════

def find_relevant_communities(keywords: list[str]) -> list[int]:
    if not keywords:
        return []
    with driver.session() as session:
        community_ids = set()
        for kw in keywords:
            result = session.run("""
                MATCH (n)
                WHERE (n:MAJOR OR n:SUBJECT OR n:SKILL OR n:CAREER OR n:TEACHER)
                  AND toLower(n.name) CONTAINS toLower($kw)
                  AND n.community_id IS NOT NULL
                RETURN DISTINCT n.community_id AS cid
                LIMIT 5
            """, kw=kw)
            for rec in result:
                community_ids.add(rec["cid"])
    return list(community_ids)


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 4: MULTI-HOP BFS TRAVERSAL
# ══════════════════════════════════════════════════════════════════════════════

def _add_node_and_paths(rec, all_nodes, all_paths):
    node_info = {
        "name":         rec["name"],
        "label":        rec["label"],
        "code":         rec["code"],
        "pagerank":     rec["pagerank"],
        "community_id": rec["community_id"],
        "hops":         rec["hops"],
    }
    all_nodes.append(node_info)
    node_names = rec["node_names"]
    rel_types  = rec["rel_types"]
    for i, rel in enumerate(rel_types):
        all_paths.append({
            "from":     node_names[i]   if i < len(node_names) else "",
            "to":       node_names[i+1] if i+1 < len(node_names) else "",
            "relation": rel,
            "hop":      i + 1,
        })


def multihop_traversal(
    keywords: list[str],
    community_ids: list[int],
    max_hops: int = MAX_HOPS,
    intent: dict | None = None
) -> tuple[list[dict], list[dict]]:

    all_nodes  = []
    all_paths  = []
    seen_names = set()

    mentioned_labels = (intent or {}).get("mentioned_labels", [])
    asked_label      = (intent or {}).get("asked_label", "UNKNOWN")
    first_mentioned  = mentioned_labels[0] if mentioned_labels else None

    # ── Phase 1: Targeted query theo intent ───────────────────────────────────
    targeted_key    = (first_mentioned, asked_label) if first_mentioned else None
    targeted_cypher = TARGETED_QUERIES.get(targeted_key) if targeted_key else None

    if targeted_cypher:
        with driver.session() as session:
            for kw in keywords:
                try:
                    results = session.run(targeted_cypher, kw=kw)
                    for rec in results:
                        _add_node_and_paths(rec, all_nodes, all_paths)
                except Exception:
                    pass

    # ── Phase 2: BFS community-filtered ──────────────────────────────────────
    with driver.session() as session:
        for kw in keywords:
            seed_rows = session.run("""
                MATCH (seed)
                WHERE (seed:MAJOR OR seed:SUBJECT OR seed:SKILL OR seed:CAREER OR seed:TEACHER)
                  AND toLower(seed.name) CONTAINS toLower($kw)
                RETURN seed
                LIMIT 3
            """, kw=kw)
            seeds = [rec["seed"] for rec in seed_rows]

            for seed in seeds:
                seed_name = seed.get("name", "")
                if seed_name in seen_names:
                    continue
                seen_names.add(seed_name)

                community_filter = ""
                params: dict = {"seed_name": seed_name, "max_hops": max_hops}

                if community_ids and asked_label not in ("UNKNOWN", None):
                    community_filter = (
                        f"AND (n.community_id IN $cids "
                        f"OR n.community_id IS NULL "
                        f"OR labels(n)[0] = '{asked_label}')"
                    )
                    params["cids"] = community_ids
                elif community_ids:
                    community_filter = "AND (n.community_id IN $cids OR n.community_id IS NULL)"
                    params["cids"] = community_ids

                traversal_query = f"""
                    MATCH path = (start)-[*1..{max_hops}]-(n)
                    WHERE start.name = $seed_name
                      AND (n:MAJOR OR n:SUBJECT OR n:SKILL OR n:CAREER OR n:TEACHER)
                      {community_filter}
                    WITH n, path,
                         [r IN relationships(path) | type(r)] AS rel_types,
                         [x IN nodes(path) | x.name]          AS node_names
                    RETURN DISTINCT
                        n.name         AS name,
                        labels(n)[0]   AS label,
                        n.code         AS code,
                        n.pagerank     AS pagerank,
                        n.community_id AS community_id,
                        rel_types,
                        node_names,
                        length(path)   AS hops
                    ORDER BY hops ASC
                    LIMIT 30
                """
                try:
                    results = session.run(traversal_query, **params)
                    for rec in results:
                        _add_node_and_paths(rec, all_nodes, all_paths)
                except Exception:
                    pass

    return all_nodes, all_paths


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 5: PAGERANK RANKING
# ══════════════════════════════════════════════════════════════════════════════

def rank_nodes(
    nodes: list[dict],
    top_k: int = TOP_K,
    negated_keywords: list[str] | None = None,
    asked_label: str | None = None
) -> list[dict]:
    negated_keywords = [kw.lower() for kw in (negated_keywords or [])]

    def score(n: dict) -> float:
        pr   = n.get("pagerank") or 0.0
        hops = n.get("hops") or 1
        return pr / hops

    # Dedup — ưu tiên bản có hops nhỏ nhất
    seen_keys: dict = {}
    for n in nodes:
        key = (n.get("label", ""), n.get("name", ""))
        if key not in seen_keys or (n.get("hops") or 99) < (seen_keys[key].get("hops") or 99):
            seen_keys[key] = n
    deduped = list(seen_keys.values())

    # Lọc thực thể bị phủ định
    if negated_keywords:
        deduped = [
            n for n in deduped
            if not any(neg in (n.get("name") or "").lower() for neg in negated_keywords)
        ]

    # 2-bucket ranking: ưu tiên asked_label
    if asked_label and asked_label != "UNKNOWN":
        target_nodes  = [n for n in deduped if n.get("label") == asked_label]
        context_nodes = [n for n in deduped if n.get("label") != asked_label]

        target_nodes.sort(key=score, reverse=True)
        context_nodes.sort(key=score, reverse=True)

        target_slots  = max(top_k // 2, min(len(target_nodes), top_k))
        context_slots = top_k - min(len(target_nodes), target_slots)

        return target_nodes[:target_slots] + context_nodes[:context_slots]
    else:
        deduped.sort(key=score, reverse=True)
        return deduped[:top_k]


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 6: RELATIONSHIP CONSTRAINT
# ══════════════════════════════════════════════════════════════════════════════

def get_relationship_constraint(intent: dict) -> str:
    mentioned = intent.get("mentioned_labels", [])
    asked     = intent.get("asked_label", "UNKNOWN")
    is_comp   = intent.get("is_comparison", False)

    if is_comp and "MAJOR" in mentioned:
        return RELATIONSHIP_CONSTRAINTS.get(("MAJOR", "MAJOR"), "")

    first_mentioned = mentioned[0] if mentioned else None
    if first_mentioned and asked and asked != "UNKNOWN":
        key = (first_mentioned, asked)
        if key in RELATIONSHIP_CONSTRAINTS:
            return RELATIONSHIP_CONSTRAINTS[key]

    for m in mentioned:
        key = (m, asked)
        if key in RELATIONSHIP_CONSTRAINTS:
            return RELATIONSHIP_CONSTRAINTS[key]

    return "Trả lời theo đúng câu hỏi, chỉ dùng dữ liệu có trong Knowledge Graph."


# ══════════════════════════════════════════════════════════════════════════════
# BƯỚC 7: GENERATE ANSWER
# ══════════════════════════════════════════════════════════════════════════════

def generate_answer(
    question: str,
    ranked_nodes: list[dict],
    traversal_paths: list[dict],
    intent: dict
) -> str:
    context = json.dumps({
        "ranked_results":   ranked_nodes,
        "traversal_paths":  traversal_paths[:60],
    }, ensure_ascii=False, indent=2)

    constraint = get_relationship_constraint(intent)

    negated = intent.get("negated_keywords", [])
    if negated:
        constraint += (
            f"\n\nLƯU Ý PHỦ ĐỊNH: Người dùng đề cập họ KHÔNG giỏi / không thích: {negated}. "
            "Loại bỏ các môn/kỹ năng/ngành này khỏi gợi ý. "
            "Thay vào đó gợi ý những lựa chọn phù hợp hơn."
        )

    system_prompt = ANSWER_SYSTEM_BASE.format(
        schema=SCHEMA_DESC,
        constraint=constraint,
    )

    no_data_hint = ""
    if not ranked_nodes:
        no_data_hint = (
            "\n[CẢNH BÁO: Không tìm thấy dữ liệu liên quan trong Knowledge Graph. "
            "Thông báo lịch sự rằng dữ liệu chưa đủ, không bịa thông tin.]"
        )

    response = ai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": (
                f"Câu hỏi: {question}\n\n"
                f"Kết quả Knowledge Graph (đã xếp hạng PageRank):\n{context}"
                f"{no_data_hint}\n\n"
                "Hướng dẫn trả lời:\n"
                "- Dùng TẤT CẢ thông tin có trong kết quả trên để trả lời.\n"
                "- Nếu có node SUBJECT với code (mã môn) → nhắc đến tên môn và mã môn.\n"
                "- Nếu có node CAREER → nhắc đến nghề nghiệp cụ thể.\n"
                "- Nếu có node SKILL → liệt kê kỹ năng.\n"
                "- KHÔNG nói 'dữ liệu chưa đủ' nếu đã có nodes trong kết quả.\n"
                "- Trả lời tự nhiên bằng tiếng Việt, kèm mã ngành/mã môn khi có:"
            )},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()


# ══════════════════════════════════════════════════════════════════════════════
# PIPELINE CHÍNH
# ══════════════════════════════════════════════════════════════════════════════

def run_pipeline(question: str, query_id: str) -> dict:
    # Bước 1: Extract intent
    intent           = extract_query_intent(question)
    keywords         = intent["keywords"]
    negated_keywords = intent["negated_keywords"]

    # Bước 2: Fetch seed entities
    seed_entities = fetch_seed_entities(keywords, intent.get("mentioned_labels", []))

    # Bước 3: Community detection
    community_ids = find_relevant_communities(keywords)

    # Bước 4: Multi-hop traversal
    raw_nodes, traversal_paths = multihop_traversal(
        keywords, community_ids, max_hops=MAX_HOPS, intent=intent
    )

    # Bước 5: PageRank ranking + negation filter
    ranked_nodes = rank_nodes(
        raw_nodes,
        top_k=TOP_K,
        negated_keywords=negated_keywords,
        asked_label=intent.get("asked_label"),
    )

    # Inject seed entities chưa có trong ranked (đảm bảo code luôn xuất hiện)
    ranked_names = {n.get("name") for n in ranked_nodes}
    extra_seeds  = [e for e in seed_entities if e.get("name") not in ranked_names]
    context_nodes = extra_seeds + ranked_nodes

    # Bước 6+7: Generate answer
    answer = generate_answer(question, context_nodes, traversal_paths, intent)

    return {
        "query_id":         query_id,
        "query":            question,
        "generated_answer": answer,
        "keywords":         keywords,
        "intent":           intent,
        "communities":      community_ids,
        "retrieved_nodes": [
            {
                "node_id":  f"node{i+1:03d}",
                "content":  json.dumps(n, ensure_ascii=False),
                "score":    round(n.get("pagerank") or 0, 6),
                "entities": [n.get("name", "")],
            }
            for i, n in enumerate(ranked_nodes)
        ],
        "traversal_paths":  traversal_paths[:20],
        "timestamp":        datetime.datetime.now().isoformat(),
    }


# ══════════════════════════════════════════════════════════════════════════════
# FASTAPI ENDPOINTS
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/metadata")
async def metadata():
    return {
        "name":        "NEU Graph Agent",
        "description": "Chatbot tư vấn đào tạo dựa trên Knowledge Graph — Đại học Kinh tế Quốc dân",
        "capabilities":       ["search", "knowledge-graph", "intent-detection", "pagerank-ranking"],
        "supported_models":   [{"model_id": OPENAI_MODEL, "name": OPENAI_MODEL}],
        "pipeline": [
            "Intent Detection (keywords, labels, negation)",
            "Seed Entity Fetch",
            "Community Detection Filter",
            "Multi-hop BFS Traversal + Targeted Queries",
            "PageRank Ranking + Negation Filter",
            "LLM Answer Generation with Relationship Constraints",
        ],
        "status": "active",
    }


@app.post("/ask")
async def ask(request: Request):
    data      = await request.json()
    question  = data.get("prompt", "").strip()
    session_id = data.get("session_id", str(uuid.uuid4()))

    if not question:
        return {
            "session_id":       session_id,
            "status":           "error",
            "content_markdown": "Vui lòng nhập câu hỏi.",
        }

    try:
        query_id = "q" + uuid.uuid4().hex[:6]
        result   = run_pipeline(question, query_id)

        return {
            "session_id":       session_id,
            "status":           "success",
            "content_markdown": result["generated_answer"],
            # Metadata debug (Portal có thể bỏ qua)
            "debug": {
                "query_id":   result["query_id"],
                "keywords":   result["keywords"],
                "intent":     result["intent"],
                "node_count": len(result["retrieved_nodes"]),
            },
        }

    except Exception as e:
        return {
            "session_id":       session_id,
            "status":           "error",
            "content_markdown": f"Đã xảy ra lỗi khi xử lý câu hỏi. Vui lòng thử lại.\n\n`{str(e)}`",
        }