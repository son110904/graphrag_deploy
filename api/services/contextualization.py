from __future__ import annotations

import json
import re
from typing import Any

from openai import OpenAI

_F = re.IGNORECASE | re.UNICODE

_VAGUE_FOLLOWUP_PATTERN = re.compile(
    r"^(?:"
    r"thế\s*còn|còn\s*(?:thì)?|rồi\s*sao|sao\s*nữa|"
    r"cái\s*đó|cái\s*này|nó\s*(?:thì)?|vậy\s*(?:còn)?|"
    r"điểm\s*chuẩn\??$|chỉ\s*tiêu\??$|học\s*phí\??$|"
    r"thời\s*gian\??$|điều\s*kiện\??$|"
    r"bao\s*nhiêu\??$|là\s*sao\??$|như\s*thế\s*nào\??$"
    r")",
    _F,
)


def question_is_vague(question: str) -> bool:
    q = (question or "").strip()
    if not q:
        return True
    if len(q) <= 18 and _VAGUE_FOLLOWUP_PATTERN.search(q.lower()):
        return True
    if re.fullmatch(r"(điểm\s*chuẩn|chỉ\s*tiêu|học\s*phí)\s*\??", q.lower(), re.UNICODE):
        return True
    return False


def extract_anchors_from_state(state: dict) -> dict[str, str | None]:
    return {
        "major_name": state.get("major_name"),
        "major_code": state.get("major_code"),
        "subject_name": state.get("subject_name"),
        "subject_code": state.get("subject_code"),
        "career_name": state.get("career_name"),
        "teacher_name": state.get("teacher_name"),
    }


def contextualize_question_with_state(question: str, state: dict) -> tuple[str, list[str], bool]:
    """
    Returns (rewritten_question, anchor_keywords, used_context).
    Heuristic: only rewrite when the question is vague and we have anchors.
    """
    anchors = extract_anchors_from_state(state or {})
    anchor_keywords: list[str] = []
    for k in ("major_name", "major_code", "subject_name", "subject_code", "career_name", "teacher_name"):
        v = anchors.get(k)
        if v:
            anchor_keywords.append(str(v))

    if not question_is_vague(question) or not anchor_keywords:
        return question, anchor_keywords, False

    q_lower = question.strip().lower()
    major = anchors.get("major_name") or anchors.get("major_code")
    subject = anchors.get("subject_name") or anchors.get("subject_code")
    career = anchors.get("career_name")
    teacher = anchors.get("teacher_name")

    if re.search(r"điểm\s*chuẩn", q_lower, re.UNICODE) and major:
        return f"Điểm chuẩn 2025 của ngành {major} tại NEU là bao nhiêu?", anchor_keywords, True
    if re.search(r"chỉ\s*tiêu", q_lower, re.UNICODE) and major:
        return f"Chỉ tiêu tuyển sinh của ngành {major} tại NEU là bao nhiêu?", anchor_keywords, True
    if re.search(r"học\s*phí", q_lower, re.UNICODE) and major:
        return f"Học phí của ngành {major} tại NEU như thế nào?", anchor_keywords, True
    if re.search(r"(môn|mã\s*môn)", q_lower, re.UNICODE) and subject:
        return f"Thông tin môn {subject} tại NEU là gì (mã môn, mô tả, mục tiêu, đánh giá)?", anchor_keywords, True
    if re.search(r"(nghề|công\s*việc|triển\s*vọng)", q_lower, re.UNICODE) and career:
        return f"Thông tin nghề {career} là gì và ngành nào tại NEU phù hợp?", anchor_keywords, True
    if re.search(r"(giảng\s*viên|thầy|cô|email)", q_lower, re.UNICODE) and teacher:
        return f"Thông tin giảng viên {teacher} (học hàm/học vị, email, môn đang dạy) là gì?", anchor_keywords, True

    if major:
        return f"{question.strip()} (ngữ cảnh: đang nói về ngành {major} tại NEU)", anchor_keywords, True
    if subject:
        return f"{question.strip()} (ngữ cảnh: đang nói về môn {subject} tại NEU)", anchor_keywords, True
    if career:
        return f"{question.strip()} (ngữ cảnh: đang nói về nghề {career})", anchor_keywords, True
    return question, anchor_keywords, False


def contextualize_question_level2(
    ai_client: OpenAI,
    model: str,
    question: str,
    history: list[dict] | None,
    summary: str,
    state: dict,
) -> tuple[str, list[str], bool]:
    """
    Level 2 contextualization with LLM (few-shot + state tracking + anchor extraction).
    Only call this when you're sure you need it (costly).
    """
    base_rewrite, anchor_keywords, used_ctx = contextualize_question_with_state(question, state)
    if not question_is_vague(question):
        return base_rewrite, anchor_keywords, used_ctx

    hist = (history or [])[-6:]
    hist_text = "\n".join([f"{m.get('role','')}: {m.get('content','')}" for m in hist]).strip()
    summary_text = (summary or "").strip()

    system = (
        "Bạn là bộ tiền xử lý truy vấn cho GraphRAG (NEO4J Knowledge Graph) của NEU.\n"
        "Nhiệm vụ: với câu hỏi hiện tại + lịch sử gần đây, hãy (1) xác định có cần ngữ cảnh không, "
        "(2) nếu cần thì viết lại câu hỏi thành dạng đầy đủ, rõ chủ thể, đúng trọng tâm, "
        "(3) trích xuất anchor entities (thực thể neo) từ lịch sử/state để hỗ trợ truy vấn graph.\n\n"
        "Ràng buộc:\n"
        "- KHÔNG trả lời nội dung tư vấn, chỉ tiền xử lý.\n"
        "- Ưu tiên bám sát lịch sử; không tự bịa ngành/môn/nghề nếu không có trong lịch sử/state.\n"
        "- Nếu câu hỏi đã standalone (đủ chủ thể) thì rewritten_question = original.\n"
        "- Output BẮT BUỘC là JSON hợp lệ, không thêm text ngoài JSON.\n"
    )

    fewshot = (
        "Ví dụ:\n"
        "History:\n"
        "user: Ngành Công nghệ thông tin học gì?\n"
        "assistant: ...\n"
        "User question: Thế còn điểm chuẩn?\n"
        "JSON:\n"
        "{\"needs_context\": true, \"standalone\": false, "
        "\"rewritten_question\": \"Điểm chuẩn 2025 của ngành Công nghệ thông tin tại NEU là bao nhiêu?\", "
        "\"anchor_entities\": [\"Công nghệ thông tin\", \"7480201\"], \"reason\": \"follow-up hỏi điểm chuẩn\"}\n\n"
        "History:\n"
        "user: Marketing khác gì Quan hệ công chúng?\n"
        "assistant: ...\n"
        "User question: so sánh kỹ hơn\n"
        "JSON:\n"
        "{\"needs_context\": true, \"standalone\": false, "
        "\"rewritten_question\": \"So sánh kỹ hơn giữa ngành Marketing và ngành Quan hệ công chúng tại NEU.\", "
        "\"anchor_entities\": [\"Marketing\", \"Quan hệ công chúng\"], \"reason\": \"follow-up so sánh\"}\n\n"
        "History:\n"
        "user: Điểm chuẩn 2025 ngành Kế toán bao nhiêu?\n"
        "assistant: ...\n"
        "User question: Chỉ tiêu bao nhiêu?\n"
        "JSON:\n"
        "{\"needs_context\": true, \"standalone\": false, "
        "\"rewritten_question\": \"Chỉ tiêu tuyển sinh của ngành Kế toán tại NEU là bao nhiêu?\", "
        "\"anchor_entities\": [\"Kế toán\", \"7340301\"], \"reason\": \"follow-up chỉ tiêu\"}\n"
    )

    user = (
        f"Session summary (nếu có): {summary_text or '—'}\n\n"
        f"History (sliding window):\n{hist_text or '—'}\n\n"
        f"State anchors (nếu có): {json.dumps(extract_anchors_from_state(state or {}), ensure_ascii=False)}\n\n"
        f"User question: {question.strip()}\n\n"
        "Hãy trả JSON theo schema:\n"
        "{\n"
        "  \"needs_context\": boolean,\n"
        "  \"standalone\": boolean,\n"
        "  \"rewritten_question\": string,\n"
        "  \"anchor_entities\": [string, ...],\n"
        "  \"reason\": string\n"
        "}\n"
    )

    try:
        resp = ai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": fewshot + "\n\n" + user},
            ],
            temperature=0,
        )
        raw = (resp.choices[0].message.content or "").strip()
        parsed = json.loads(raw)
        rewritten = str(parsed.get("rewritten_question") or "").strip() or question
        anchor = parsed.get("anchor_entities") or []
        if not isinstance(anchor, list):
            anchor = []
        anchor = [str(x).strip() for x in anchor if str(x).strip()]

        merged_anchor = list(dict.fromkeys([*anchor_keywords, *anchor]))
        needs_ctx = bool(parsed.get("needs_context"))
        if not needs_ctx:
            return question, merged_anchor, False
        return rewritten, merged_anchor, True
    except Exception as e:
        print(f"  [level2 contextualize] WARNING: {e}")
        return base_rewrite, anchor_keywords, used_ctx


def update_session_summary_level2(
    ai_client: OpenAI,
    model: str,
    prev_summary: str,
    history: list[dict] | None,
) -> str:
    hist = (history or [])[-8:]
    hist_text = "\n".join([f"{m.get('role','')}: {m.get('content','')}" for m in hist]).strip()
    if not hist_text:
        return (prev_summary or "").strip()

    system = (
        "Bạn là bộ nhớ tóm tắt cho chatbot NEU. "
        "Hãy cập nhật 'session summary' ngắn gọn, tập trung vào: chủ đề đang hỏi, thực thể chính "
        "(ngành/môn/nghề/chương trình), và mục tiêu người dùng.\n"
        "Output chỉ 1 đoạn ngắn (1-2 câu), không bullet, không markdown."
    )
    user = (
        f"Previous summary (có thể rỗng): {prev_summary or '—'}\n\n"
        f"Recent turns:\n{hist_text}\n\n"
        "Hãy viết summary mới:"
    )
    try:
        resp = ai_client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
            temperature=0,
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"  [summary] WARNING: {e}")
        return (prev_summary or "").strip()


def update_session_state_from_result(state: dict, result: dict) -> dict:
    state = dict(state or {})
    retrieved = result.get("retrieved_nodes") or []
    for item in retrieved:
        try:
            payload = json.loads(item.get("content") or "{}")
        except Exception:
            continue
        label = (payload.get("label") or "").upper()
        name = payload.get("name")
        code = payload.get("code")
        if label == "MAJOR" and name and not state.get("major_name"):
            state["major_name"] = name
            if code:
                state["major_code"] = code
        elif label == "SUBJECT" and name and not state.get("subject_name"):
            state["subject_name"] = name
            if code:
                state["subject_code"] = code
        elif label == "CAREER" and name and not state.get("career_name"):
            state["career_name"] = name
        elif label == "TEACHER" and name and not state.get("teacher_name"):
            state["teacher_name"] = name
        if (
            state.get("major_name")
            and state.get("subject_name")
            and state.get("career_name")
            and state.get("teacher_name")
        ):
            break
    return state


__all__ = [
    "contextualize_question_with_state",
    "contextualize_question_level2",
    "extract_anchors_from_state",
    "question_is_vague",
    "update_session_state_from_result",
    "update_session_summary_level2",
]

