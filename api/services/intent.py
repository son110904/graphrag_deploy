from __future__ import annotations

import json
import re

from openai import OpenAI

_F = re.IGNORECASE | re.UNICODE


_MBTI_PATTERN = re.compile(
    r"\b(INTJ|INTP|ENTJ|ENTP|INFJ|INFP|ENFJ|ENFP"
    r"|ISTJ|ISFJ|ESTJ|ESFJ|ISTP|ISFP|ESTP|ESFP)\b",
    re.IGNORECASE,
)


# Map MBTI code → keywords để mở rộng query khi DB chưa có SUITS_MAJOR/SUITS_CAREER
MBTI_KEYWORD_FALLBACK: dict[str, list[str]] = {
    "INTJ": ["chiến lược", "phân tích", "độc lập", "tầm nhìn"],
    "INTP": ["phân tích", "logic", "nghiên cứu", "lý luận"],
    "ENTJ": ["lãnh đạo", "chiến lược", "quyết đoán", "quản lý"],
    "ENTP": ["sáng tạo", "đổi mới", "lập luận", "linh hoạt"],
    "INFJ": ["đồng cảm", "tầm nhìn", "sáng tạo", "kiên nhẫn"],
    "INFP": ["sáng tạo", "đồng cảm", "lý tưởng", "linh hoạt"],
    "ENFJ": ["lãnh đạo", "đồng cảm", "giao tiếp", "tổ chức"],
    "ENFP": ["sáng tạo", "nhiệt huyết", "giao tiếp", "linh hoạt"],
    "ISTJ": ["kỷ luật", "cẩn thận", "trách nhiệm", "tổ chức"],
    "ISFJ": ["đồng cảm", "kiên nhẫn", "cẩn thận", "hỗ trợ"],
    "ESTJ": ["tổ chức", "kỷ luật", "lãnh đạo", "quyết đoán"],
    "ESFJ": ["giao tiếp", "đồng cảm", "hỗ trợ", "tổ chức"],
    "ISTP": ["phân tích", "thực tế", "kỹ thuật", "linh hoạt"],
    "ISFP": ["sáng tạo", "thực tế", "đồng cảm", "linh hoạt"],
    "ESTP": ["năng động", "thực tế", "quyết đoán", "lãnh đạo"],
    "ESFP": ["năng động", "giao tiếp", "linh hoạt", "thực tế"],
}


def expand_mbti(question: str) -> tuple[str, list[str]]:
    m = _MBTI_PATTERN.search(question)
    if not m:
        return question, []
    mbti_code = m.group(1).upper()
    hint = f"[GHI CHÚ: {mbti_code} là loại tính cách MBTI]"
    return question + "  " + hint, [mbti_code]


ABBREVIATION_MAP: dict[str, list[str]] = {
    "da":   ["data analyst", "phân tích dữ liệu"],
    "de":   ["data engineer", "kỹ sư dữ liệu"],
    "ds":   ["data scientist", "khoa học dữ liệu"],
    "data analyst":     ["phân tích dữ liệu", "chuyên viên phân tích dữ liệu"],
    "data engineer":    ["kỹ sư dữ liệu"],
    "data scientist":   ["khoa học dữ liệu", "nhà khoa học dữ liệu"],
    "data engineering": ["kỹ sư dữ liệu"],
    "data analysis":    ["phân tích dữ liệu"],
    "ba":   ["business analyst", "phân tích kinh doanh"],
    "pm":   ["project manager", "quản lý dự án"],
    "po":   ["product owner"],
    "qa":   ["kiểm thử", "quality assurance"],
    "dev":  ["lập trình viên", "developer"],
    "fe":   ["front end", "lập trình viên frontend"],
    "be":   ["back end", "lập trình viên backend"],
    "ml":   ["machine learning", "học máy"],
    "ai":   ["trí tuệ nhân tạo", "artificial intelligence"],
    "cntt": ["công nghệ thông tin"],
    "ktpm": ["kỹ thuật phần mềm"],
    "httt": ["hệ thống thông tin"],
    "qtkd": ["quản trị kinh doanh"],
    "tcnh": ["tài chính ngân hàng"],
    "kt":   ["kế toán", "kinh tế"],
    "mkt":  ["marketing"],
    "hr":   ["quản trị nhân lực", "nhân sự"],
    "mis":  ["hệ thống thông tin quản lý", "management information systems"],
    "fintech": ["công nghệ tài chính"],
    "ecom": ["thương mại điện tử"],
    "acct": ["kế toán"],
}


def expand_abbreviations(question: str) -> tuple[str, list[str]]:
    q_lower = question.lower()
    expanded = question
    extras: list[str] = []
    found: dict[str, list[str]] = {}

    for abbrev, expansions in ABBREVIATION_MAP.items():
        if len(abbrev) <= 3:
            pat = r"(?<![\w\u00C0-\u024F])" + re.escape(abbrev.upper()) + r"(?![\w\u00C0-\u024F])"
            if not re.search(pat, question, re.UNICODE):
                continue
        pattern = r"(?<![\w\u00C0-\u024F])" + re.escape(abbrev) + r"(?![\w\u00C0-\u024F])"
        if re.search(pattern, q_lower, _F):
            found[abbrev] = expansions
            extras.extend(expansions)

    if found:
        hints = "; ".join(f"{k.upper()} = {' / '.join(v)}" for k, v in found.items())
        expanded = question + f"  [GHI CHÚ: {hints}]"

    return expanded, extras


def extract_query_intent(
    ai_client: OpenAI,
    model: str,
    question: str,
    intent_taxonomy_hint: str,
) -> dict:
    system_msg = (
        "Bạn phân tích câu hỏi tư vấn học thuật và trả về JSON.\n"
        "Schema Node labels: MAJOR, SUBJECT, SKILL, CAREER, TEACHER, PERSONALITY\n\n"
        "Chuẩn hóa keyword:\n"
        "  data analyst/DA → phân tích dữ liệu, data analyst\n"
        "  business analyst/BA → phân tích kinh doanh\n"
        "  CNTT/IT → công nghệ thông tin\n"
        "  KTPM → kỹ thuật phần mềm | HTTT → hệ thống thông tin\n"
        "  developer/DEV → lập trình viên | tester/QA → kiểm thử\n\n"
        f"{intent_taxonomy_hint}\n\n"
        "Quy tắc xác định asked_label:\n"
        "  - Hỏi thông tin môn học (mô tả, mã môn, nội dung, kế hoạch giảng dạy) → asked=SUBJECT\n"
        "  - Hỏi thông tin nghề nghiệp (mô tả nghề, công việc, thị trường lao động, triển vọng, cơ hội nghề nghiệp) → asked=CAREER\n"
        "  - Hỏi thông tin giảng viên (email, học hàm, dạy môn gì) → asked=TEACHER\n"
        "  - Hỏi thông tin ngành học (chương trình, chuẩn đầu ra, mục tiêu) → asked=MAJOR\n"
        "  - Hỏi kỹ năng → asked=SKILL\n"
        "  - Hỏi về loại tính cách MBTI, personality fit, đặc điểm tính cách → asked=PERSONALITY\n"
        "  - Nếu đề cập tính cách/MBTI nhưng hỏi về nghề → mentioned=PERSONALITY, asked=CAREER\n"
        "  - Nếu đề cập tính cách/MBTI nhưng hỏi về ngành → mentioned=PERSONALITY, asked=MAJOR\n"
        "  - Keywords: luôn giữ nguyên MBTI code (ESTP, ENTP...) nếu có\n\n"
        "──────────────────────────────────────────\n"
        "TRƯỜNG ĐẶC BIỆT: mbti_dimensions\n"
        "──────────────────────────────────────────\n"
        "Nếu câu hỏi mô tả đặc điểm tính cách bằng từ ngữ tự nhiên (KHÔNG phải MBTI code),\n"
        "hãy suy luận các MBTI dimension letters phù hợp:\n\n"
        "  4 cặp dimension:\n"
        "    E / I  — năng lượng:  hướng ngoại (E) vs hướng nội, điềm tĩnh, kín đáo, suy tư (I)\n"
        "    S / N  — nhận thức:   thực tế, chi tiết, quy trình (S) vs sáng tạo, tầm nhìn, trực giác (N)\n"
        "    T / F  — quyết định:  logic, phân tích, lý trí (T) vs đồng cảm, ấm áp, cảm xúc (F)\n"
        "    J / P  — lối sống:    kế hoạch, ngăn nắp, kỷ luật (J) vs linh hoạt, ngẫu hứng, tự do (P)\n\n"
        "  Quy tắc:\n"
        "  - Chỉ trả về dimension mà câu hỏi có dấu hiệu rõ ràng. Không đoán mò.\n"
        "  - Nếu câu hỏi có cả 2 chiều đối lập (E lẫn I), bỏ cả 2, không trả về dimension đó.\n"
        "  - Nếu câu hỏi có MBTI code tường minh (INTJ, ESTP...), để mbti_dimensions = []\n"
        "    và đưa code đó vào keywords thay vào đó.\n"
        "  - Nếu không có dấu hiệu tính cách nào, để mbti_dimensions = [].\n\n"
        "Trả về JSON:\n"
        "{\n"
        '  "keywords": ["tên thực thể để tìm trong KG"],\n'
        '  "mentioned_labels": ["MAJOR|SUBJECT|SKILL|CAREER|TEACHER|PERSONALITY"],\n'
        '  "asked_label": "MAJOR|SUBJECT|SKILL|CAREER|TEACHER|PERSONALITY|UNKNOWN",\n'
        '  "negated_keywords": ["thực thể bị phủ định"],\n'
        '  "is_comparison": false,\n'
        '  "mbti_dimensions": ["I","T"]\n'
        "}\n"
    )
    response = ai_client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Phân tích: {question}"},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    parsed = json.loads(response.choices[0].message.content)
    return {
        "keywords": parsed.get("keywords", []),
        "mentioned_labels": parsed.get("mentioned_labels", []),
        "asked_label": parsed.get("asked_label", "UNKNOWN"),
        "negated_keywords": parsed.get("negated_keywords", []),
        "is_comparison": parsed.get("is_comparison", False),
        "mbti_dimensions": [
            d for d in parsed.get("mbti_dimensions", [])
            if d in ("E", "I", "S", "N", "T", "F", "J", "P")
        ],
    }


def resolve_mbti_codes_from_dimensions(dimensions: list[str]) -> list[str]:
    if not dimensions:
        return []
    all_types = [
        "INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ", "ISTP", "ISFP", "ESTP", "ESFP",
    ]
    required = set(dimensions)
    return [t for t in all_types if required.issubset(set(t))]


_COMPARE_CUE_PATTERN = re.compile(
    r"\b(vs|versus)\b|so sánh|phân vân|giữa.+và|nên chọn bên nào|nên chọn cái nào"
    r"|nên học.{0,30}hay.{0,30}(ngành|chuyên ngành)"
    r"|(ngành|chuyên ngành).{0,30}hay.{0,30}(ngành|chuyên ngành)"
    r"|không biết (nên|phải) chọn|chưa biết (nên|chọn)|đang phân vân"
    r"|so (với|sánh với)|khác nhau (như thế nào|ra sao|thế nào)",
    _F,
)
_CAREER_CUE_PATTERN = re.compile(
    r"nghề nào|làm gì|ra trường làm gì|nên chọn nghề|nên theo nghề|hợp làm|hợp nghề",
    _F,
)
_ASK_PERSONALITY_PATTERN = re.compile(r"tính cách (gì|nào)|mbti (gì|nào)|loại tính cách", _F)
_MAJOR_CUE_PATTERN = re.compile(r"\bngành\b|chuyên ngành|chương trình đào tạo|học ngành", _F)
_SKILL_CUE_PATTERN = re.compile(r"\bsql\b|database|cơ sở dữ liệu|dữ liệu|data", _F)
_NEGATED_CAREER_PATTERN = re.compile(r"(?:không|ko|chẳng|không muốn).{0,20}\b(sale|marketing)\b", _F)
_MAJOR_EXCLUDE_SKILL_PATTERN = re.compile(
    r"ng[àa]nh\s*(n[àa]o)?.{0,20}(kh[oô]ng\s*(c[aầ]n|y[eê]u\s*c[aầ]u|đ[oò]i|ph[aả]i)|"
    r"kh[oô]ng\s*c[aầ]n\s*ph[aả]i|mi[eễ]n\s*(kh[oô]ng\s*)?ph[aả]i|kh[oô]ng\s*dùng)"
    r".{0,40}",
    _F,
)

_PERSONALITY_KW_PATTERN = re.compile(
    r"tính cách|phẩm chất|personality|hướng nội|hướng ngoại|"
    r"cẩn thận|sáng tạo|lãnh đạo|đồng cảm|kiên nhẫn|tự tin|"
    r"điềm tĩnh|sâu sắc|kín đáo|nội tâm|tập trung|thận trọng|"
    r"suy tư|ôn hòa|trầm mặc|tinh tế|logic|phân tích|lý trí|"
    r"thấu cảm|ấm áp|nhân văn|nề nếp|kế hoạch|tổ chức|ngăn nắp|"
    r"linh hoạt|tự do|ngẫu hứng|thoải mái|phóng khoáng|"
    r"chiến lược|tầm nhìn|lý tưởng|đổi mới|tò mò|khám phá|"
    r"kỷ luật|trách nhiệm|quyết đoán|"
    r"hợp\s+(với\s+)?(nghề|ngành)|phù hợp\s+(với\s+)?(tôi|mình|người)|"
    r"\b(INTJ|INTP|ENTJ|ENTP|INFJ|INFP|ENFJ|ENFP"
    r"|ISTJ|ISFJ|ESTJ|ESFJ|ISTP|ISFP|ESTP|ESFP)\b",
    _F,
)

_CAREER_ALIAS_HINTS: list[tuple[re.Pattern, list[str]]] = [
    (re.compile(r"\b(tester|qa|quality assurance|kiểm thử)\b", _F), ["kiểm thử", "tester", "quality assurance"]),
    (re.compile(r"\b(developer|dev|lập trình viên)\b", _F), ["lập trình viên", "developer"]),
]
_DOMAIN_HINTS: list[tuple[re.Pattern, list[str], list[str]]] = [
    (re.compile(r"\b(cntt|it|công nghệ thông tin)\b", _F), ["công nghệ thông tin"], ["MAJOR"]),
    (re.compile(r"\b(database|cơ sở dữ liệu)\b", _F), ["database"], ["SKILL"]),
    (re.compile(r"\bsql\b", _F), ["sql"], ["SKILL"]),
]
_FIELD_CONTEXT_HINTS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\b(cntt|it|công nghệ thông tin|lập trình|phần mềm|kỹ thuật phần mềm|hệ thống thông tin)\b", _F), "Công nghệ thông tin"),
    (re.compile(r"\b(kinh tế|tài chính|kế toán|ngân hàng|kinh doanh|quản trị|marketing)\b", _F), "Kinh tế - Quản trị"),
    (re.compile(r"\b(data|dữ liệu|phân tích dữ liệu|khoa học dữ liệu)\b", _F), "Khoa học dữ liệu"),
    (re.compile(r"\b(giáo dục|sư phạm|giảng dạy|đào tạo)\b", _F), "Giáo dục"),
    (re.compile(r"\b(y tế|bác sĩ|y khoa|dược|chăm sóc sức khỏe)\b", _F), "Y tế - Sức khỏe"),
]


def unique_keep_order(values: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for v in values:
        sv = str(v).strip()
        if not sv:
            continue
        key = sv.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(sv)
    return out


def apply_intent_rules(question: str, intent: dict) -> dict:
    q = question.strip()
    q_lower = q.lower()

    keywords = unique_keep_order([*intent.get("keywords", [])])
    mentioned = [str(x).strip().upper() for x in intent.get("mentioned_labels", []) if str(x).strip()]
    mentioned = unique_keep_order(mentioned)
    asked = str(intent.get("asked_label", "UNKNOWN")).upper()
    negated = unique_keep_order([*intent.get("negated_keywords", [])])
    is_comp = bool(intent.get("is_comparison", False))

    for pat, kws, labels in _DOMAIN_HINTS:
        if pat.search(q):
            keywords.extend(kws)
            mentioned.extend(labels)

    has_direct_career_alias = False
    for pat, kws in _CAREER_ALIAS_HINTS:
        if pat.search(q):
            has_direct_career_alias = True
            keywords.extend(kws)
            if "CAREER" not in mentioned:
                mentioned.append("CAREER")

    for m in _NEGATED_CAREER_PATTERN.finditer(q):
        neg_kw = m.group(1).strip()
        if neg_kw not in negated:
            negated.append(neg_kw)

    if _COMPARE_CUE_PATTERN.search(q):
        is_comp = True

    has_personality_signal = "PERSONALITY" in mentioned or _PERSONALITY_KW_PATTERN.search(q)

    if _ASK_PERSONALITY_PATTERN.search(q):
        asked = "PERSONALITY"
        for pat, field_name in _FIELD_CONTEXT_HINTS:
            if pat.search(q):
                intent["field_context"] = field_name
                break

    if is_comp and has_direct_career_alias:
        asked = "CAREER"

    if is_comp and not has_direct_career_alias and not _CAREER_CUE_PATTERN.search(q):
        if "MAJOR" not in mentioned:
            mentioned.append("MAJOR")
        if asked in ("UNKNOWN", "CAREER") and not has_direct_career_alias:
            asked = "MAJOR"

    if _MAJOR_EXCLUDE_SKILL_PATTERN.search(q):
        asked = "MAJOR"
        if "MAJOR" not in mentioned:
            mentioned.append("MAJOR")

    if asked == "UNKNOWN":
        if _CAREER_CUE_PATTERN.search(q):
            asked = "CAREER"
        elif has_personality_signal and (_SKILL_CUE_PATTERN.search(q) or bool(negated)):
            asked = "CAREER"
        elif _MAJOR_CUE_PATTERN.search(q):
            asked = "MAJOR"

    if asked == "PERSONALITY":
        is_asking_personality_explicitly = bool(_ASK_PERSONALITY_PATTERN.search(q))
        if is_asking_personality_explicitly:
            pass
        elif _CAREER_CUE_PATTERN.search(q) and "CAREER" in mentioned:
            asked = "CAREER"
        elif _MAJOR_CUE_PATTERN.search(q) and "MAJOR" in mentioned and "CAREER" not in mentioned:
            asked = "MAJOR"

    if asked == "CAREER":
        priority = ["CAREER", "SKILL", "MAJOR", "PERSONALITY", "SUBJECT", "TEACHER"] if is_comp else \
                   ["SKILL", "MAJOR", "PERSONALITY", "CAREER", "SUBJECT", "TEACHER"]
    elif asked == "MAJOR":
        priority = ["MAJOR", "SKILL", "PERSONALITY", "CAREER", "SUBJECT", "TEACHER"] if negated else \
                   ["PERSONALITY", "SKILL", "CAREER", "MAJOR", "SUBJECT", "TEACHER"]
    elif asked == "PERSONALITY":
        if re.search(r"hợp làm|hợp nghề|làm\s+\w+", q_lower, _F):
            priority = ["CAREER", "MAJOR", "PERSONALITY", "SKILL", "SUBJECT", "TEACHER"]
        else:
            priority = ["MAJOR", "CAREER", "PERSONALITY", "SKILL", "SUBJECT", "TEACHER"]
    else:
        priority = ["PERSONALITY", "SKILL", "MAJOR", "CAREER", "SUBJECT", "TEACHER"]

    mentioned_set = set(mentioned)
    mentioned = [lbl for lbl in priority if lbl in mentioned_set]
    mentioned.extend([lbl for lbl in mentioned_set if lbl not in mentioned])

    intent["keywords"] = unique_keep_order(keywords)
    intent["mentioned_labels"] = mentioned
    intent["asked_label"] = asked if asked in {"MAJOR", "SUBJECT", "SKILL", "CAREER", "TEACHER", "PERSONALITY", "UNKNOWN"} else "UNKNOWN"
    intent["negated_keywords"] = unique_keep_order(negated)
    intent["is_comparison"] = is_comp
    return intent


__all__ = [
    "ABBREVIATION_MAP",
    "MBTI_KEYWORD_FALLBACK",
    "apply_intent_rules",
    "expand_abbreviations",
    "expand_mbti",
    "extract_query_intent",
    "resolve_mbti_codes_from_dimensions",
]

