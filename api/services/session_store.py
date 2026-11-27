"""
Lưu bền bộ nhớ hội thoại (context window) vào Neo4j.

Mỗi phiên chat là một node :ChatSession {session_id} lưu:
  - history: JSON string — danh sách {role, content} tối đa MAX_HISTORY_MESSAGES
  - state:   JSON string — anchor entities (major/subject/career/teacher)
  - summary: string      — tóm tắt ý định (level-2 contextualization)
  - updated_at: ISO timestamp

Tái dùng Neo4j driver sẵn có, không thêm hạ tầng mới. Mọi lỗi I/O được
nuốt (fail-safe) để không bao giờ làm hỏng response của người dùng — khi DB
không truy cập được, hệ thống đơn giản mất tính "ghi nhớ" cho lượt đó.
"""

import json
import datetime

# 5 lượt hội thoại = 10 messages (user + assistant), giữ đồng bộ với bản cũ.
MAX_HISTORY_MESSAGES = 10

# Cờ chặn tạo constraint lặp lại trong cùng process (lazy, không cần startup hook).
_schema_ready = {"done": False}


def _loads(raw, default):
    """Parse JSON string an toàn, trả về `default` nếu rỗng/hỏng."""
    if not raw:
        return default
    try:
        value = json.loads(raw)
        return value if value is not None else default
    except Exception:
        return default


def ensure_schema(driver) -> None:
    """Tạo unique constraint cho ChatSession.session_id (idempotent, chạy 1 lần)."""
    if _schema_ready["done"]:
        return
    try:
        with driver.session() as s:
            s.run(
                "CREATE CONSTRAINT chat_session_id IF NOT EXISTS "
                "FOR (c:ChatSession) REQUIRE c.session_id IS UNIQUE"
            )
        _schema_ready["done"] = True
    except Exception:
        # Thiếu quyền tạo constraint vẫn không chặn luồng chính; MERGE vẫn chạy được.
        pass


def load_session(driver, session_id: str) -> tuple[list[dict], dict, str]:
    """
    Nạp bộ nhớ của một phiên từ Neo4j.

    Trả về (history, state, summary). Nếu chưa có phiên hoặc lỗi → ([], {}, "").
    """
    ensure_schema(driver)
    try:
        with driver.session() as s:
            rec = s.run(
                "MATCH (c:ChatSession {session_id: $sid}) "
                "RETURN c.history AS history, c.state AS state, c.summary AS summary",
                sid=session_id,
            ).single()
    except Exception:
        return [], {}, ""

    if not rec:
        return [], {}, ""

    history = _loads(rec.get("history"), [])
    if not isinstance(history, list):
        history = []
    state = _loads(rec.get("state"), {})
    if not isinstance(state, dict):
        state = {}
    summary = rec.get("summary") or ""

    # Cắt an toàn phòng khi dữ liệu cũ dài hơn giới hạn hiện tại.
    if len(history) > MAX_HISTORY_MESSAGES:
        history = history[-MAX_HISTORY_MESSAGES:]
    return history, state, summary


def save_session(driver, session_id: str, history: list[dict], state: dict, summary: str) -> None:
    """Ghi (upsert) bộ nhớ của một phiên xuống Neo4j. Fail-safe."""
    try:
        trimmed = list(history or [])[-MAX_HISTORY_MESSAGES:]
        with driver.session() as s:
            s.run(
                "MERGE (c:ChatSession {session_id: $sid}) "
                "SET c.history = $history, "
                "    c.state = $state, "
                "    c.summary = $summary, "
                "    c.updated_at = $ts",
                sid=session_id,
                history=json.dumps(trimmed, ensure_ascii=False),
                state=json.dumps(state or {}, ensure_ascii=False),
                summary=summary or "",
                ts=datetime.datetime.utcnow().isoformat(),
            )
    except Exception:
        # Không làm hỏng response nếu ghi thất bại.
        pass


def append_turn(history: list[dict], question: str, answer: str) -> list[dict]:
    """Thêm 1 lượt (user + assistant) và cắt về cửa sổ tối đa."""
    merged = list(history or [])
    merged.append({"role": "user", "content": question})
    merged.append({"role": "assistant", "content": answer})
    return merged[-MAX_HISTORY_MESSAGES:]
