from __future__ import annotations

import re

_F = re.IGNORECASE | re.UNICODE

_TUITION_KEYWORDS = re.compile(
    r"học phí|tiền học|chi phí học|mức phí|phí đào tạo|đóng tiền|nộp tiền"
    r"|học bổng.*tiền|tiền.*học bổng"
    r"|giá học|bao nhiêu tiền|tốn bao nhiêu|chi phí.*(?:ngành|khoá|chương trình)"
    r"|(?:ngành|khoá|chương trình).*chi phí"
    r"|phí.*(?:ngành|khoá|học kỳ|năm học)"
    r"|(?:ngành|khoá|học kỳ|năm học).*phí"
    r"|học kỳ.*tiền|tiền.*học kỳ"
    r"|đóng.*(?:học phí|tiền)|(?:học phí|tiền).*đóng",
    _F,
)


def detect_tuition_question(question: str) -> bool:
    return bool(_TUITION_KEYWORDS.search((question or "").strip()))


_SELF_INTRO_PATTERN = re.compile(
    r"bạn (là|là gì|là ai|có thể|làm được|giúp được|biết gì|dùng để làm|làm gì|làm đc gì|lm đc gì)\b"
    r"|bạn tên (là |gì)\b"
    r"|(?:giới thiệu|tự giới thiệu).{0,20}(?:bạn|mình|bản thân)\b"
    r"|(?:chatbot|trợ lý|bot).{0,30}(?:này|đây|là gì|làm gì|có thể)\b"
    r"|(?:bạn|mày|m) có (?:thể|biết|làm|hiểu)\b"
    r"|(?:chào|hello|hi|xin chào).{0,30}(?:bạn|bot|chatbot)\b"
    r"|bạn có thể giúp gì|bạn hỗ trợ gì|bạn giải đáp gì"
    r"|chatbot này là gì|chatbot này làm gì|chatbot này dùng để làm gì"
    r"|bạn có thể trả lời (về|câu hỏi) gì|bạn có thể tư vấn"
    r"|bạn biết gì|bạn hiểu gì|bạn trả lời được gì"
    r"|em có thể hỏi gì|tôi có thể hỏi gì|mình có thể hỏi gì"
    r"|nội dung gì|về nội dung|giải đáp.*nội dung"
    r"|bạn tư vấn|tư vấn (về|gì|những gì|được gì|về gì)"
    r"|bạn (giúp|hỗ trợ|trả lời).{0,15}(gì|được gì|những gì)"
    r"|(?:cho tôi|cho mình|cho em).{0,20}biết.{0,20}(?:bạn|chatbot|bot)",
    _F,
)

_META_PATTERNS = _SELF_INTRO_PATTERN


def detect_self_intro(question: str) -> bool:
    return bool(_SELF_INTRO_PATTERN.search(question or ""))


def detect_meta_question(question: str) -> bool:
    return detect_self_intro(question)


SELF_INTRO_ANSWER = """
Xin chào! Tôi là **NEU AI Assistant**.

Tôi là chatbot hỗ trợ hỏi đáp học thuật về Đại học Kinh tế Quốc dân (NEU).

Tôi có thể giúp bạn:
• Tìm hiểu ngành học và chương trình đào tạo  
• Tra cứu môn học và nội dung môn  
• Tìm giảng viên dạy môn  
• Khám phá kỹ năng từ từng môn học  
• Tìm mối liên hệ giữa ngành học – kỹ năng – nghề nghiệp

Tôi sử dụng **Knowledge Graph + GraphRAG + Neo4j** để truy vấn và tổng hợp thông tin chính xác.

Bạn muốn hỏi gì về việc học tại NEU? 😊
"""

CHATBOT_IDENTITY = SELF_INTRO_ANSWER


_SCORE_CONVERT_STRONG_PATTERN = re.compile(
    r"quy\s*đổi\s*điểm|quy\s*đổi\s*chứng\s*chỉ|điểm\s*quy\s*đổi"
    r"|quy\s*đổi|đổi\s*điểm|tính\s*điểm\s*xét\s*tuyển|công\s*thức\s*điểm"
    r"|\b(ielts|toefl|toeic|sat|act|hsa|v\-?act|tsa)\b"
    r"|ccta?q?t|chứng\s*chỉ\s*tiếng\s*anh\s*quốc\s*tế"
    r"|điểm\s*sàn|ngưỡng\s*đầu\s*vào|điểm\s*ưu\s*tiên|cộng\s*điểm\s*ưu\s*tiên"
    r"|kv1|kv2|kv3|ưu\s*tiên\s*(?:khu\s*vực|đối\s*tượng)",
    _F,
)

_SCORE_CONVERT_MATH_PATTERN = re.compile(
    r"(?:(?:\+|\-|\*|/)\s*\d+(?:[.,]\d+)?)"
    r"|(?:\d+(?:[.,]\d+)?\s*(?:\+|\-|\*|/)\s*\d+(?:[.,]\d+)?)",
    re.UNICODE,
)

_ADMISSION_INFO_STRONG_PATTERN = re.compile(
    r"phương\s*thức\s*xét\s*tuyển|xét\s*tuyển\s*kết\s*hợp|\bxtkh\b"
    r"|xét\s*tuyển\s*thẳng|điều\s*kiện\s*(?:xét\s*tuyển|dự\s*tuyển|tuyển\s*sinh)"
    r"|hồ\s*sơ\s*xét\s*tuyển|nộp\s*hồ\s*sơ|đăng\s*ký\s*xét\s*tuyển|đăng\s*ký|đăng\s*kí"
    r"|lịch\s*tuyển\s*sinh|lộ\s*trình\s*tuyển\s*sinh|kế\s*hoạch\s*tuyển\s*sinh"
    r"|khi\s*nào\s*nộp|bao\s*giờ\s*nộp|hạn\s*nộp|deadline|thời\s*hạn|mốc\s*thời\s*gian"
    r"|ngưỡng\s*đầu\s*vào|điểm\s*sàn|điểm\s*liệt|điểm\s*ưu\s*tiên"
    r"|ưu\s*tiên\s*(?:khu\s*vực|đối\s*tượng)|kv1|kv2|kv3"
    r"|open\s*day|tư\s*vấn\s*tuyển\s*sinh|hotline\s*tuyển\s*sinh"
    r"|neu\s*20\d{2}|tuyển\s*sinh\s*20\d{2}|ngành\s*mới\s*20\d{2}|chương\s*trình\s*mới\s*20\d{2}",
    _F,
)

_ADMISSION_SAFE = re.compile(
    r"điểm\s*chuẩn|chỉ\s*tiêu"
    r"|điểm\s*\d+(?:[.,]\d+)?\s*(?:có\s*)?(?:vào|đỗ|đậu|trúng)\s*(?:được\s*)?(?:ngành|trường|neu)"
    r"|điểm\s*\d+(?:[.,]\d+)?\s*(?:thì|là)\s*(?:vào|đỗ|đậu|học)\s*(?:được\s*)?(?:ngành|ngành\s*nào)"
    r"|điểm\s*\d+(?:[.,]\d+)?\s*(?:tổ\s*hợp\s*)?(?:a00|a01|b00|b01|c00|d01|d07)\b"
    r"|ngành\s+.+\s+năm\s+20\d{2}\s+điểm\s*chuẩn\s+bao\s*nhiêu"
    r"|môn\s+học|giảng\s+viên|kỹ\s+năng|nghề\s+nghiệp|hướng\s*nghiệp",
    _F,
)


SCORE_CONVERT_ANSWER = (
    "Câu hỏi của bạn liên quan đến **quy đổi và tư vấn điểm xét tuyển** — "
    "lĩnh vực này được xử lý bởi agent chuyên biệt.\n\n"
    "👉 Vui lòng sử dụng agent **Quy đổi và tư vấn điểm**\n"
    "**https://ai.neu.edu.vn/tuyen-sinh/tools/convertum**\n\n"
    "Agent này hỗ trợ:\n"
    "- Quy đổi điểm từ: IELTS, TOEFL iBT, TOEIC, SAT, ACT, HSA, V-ACT, TSA\n"
    "- Điểm thi THPT (các tổ hợp A00/A01/D01/D07)\n"
    "- Tính điểm ưu tiên khu vực/đối tượng\n"
    "- Tư vấn ngành nào phù hợp với điểm của bạn"
)

ADMISSION_INFO_ANSWER = (
    "Câu hỏi của bạn liên quan đến **thông tin tuyển sinh NEU 2026** "
    "(quy chế, phương thức, lộ trình, học phí...) — "
    "lĩnh vực này được xử lý bởi agent chuyên biệt.\n\n"
    "👉 Vui lòng sử dụng agent **Thông tin tuyển sinh NEU 2026** tại:\n"
    "**https://ai.neu.edu.vn/tuyen-sinh/tools/neu-admission-info**\n\n"
    "Agent này có đầy đủ:\n"
    "- Quy chế & điều kiện bắt buộc\n"
    "- Phương thức xét tuyển (thẳng, kết hợp, THPT)\n"
    "- Tra cứu chỉ tiêu & điểm chuẩn 2025\n"
    "- Quy đổi chứng chỉ tiếng Anh quốc tế\n"
    "- Lộ trình tuyển sinh & kênh liên hệ chính thức\n\n"
    "Tôi vẫn có thể giúp bạn tra cứu **điểm chuẩn/chỉ tiêu từng ngành** "
    "hoặc tư vấn **ngành học phù hợp** nếu bạn cần!"
)


def detect_score_convert(question: str) -> bool:
    if _SCORE_CONVERT_STRONG_PATTERN.search(question or "") or _SCORE_CONVERT_MATH_PATTERN.search(question or ""):
        return True
    if _ADMISSION_SAFE.search(question or ""):
        return False
    return False


def detect_admission_info(question: str) -> bool:
    if _ADMISSION_INFO_STRONG_PATTERN.search(question or ""):
        if detect_score_convert(question):
            return False
        return True
    if _ADMISSION_SAFE.search(question or ""):
        return False
    return False


_OFF_TOPIC_PATTERNS = [
    re.compile(r"thời tiết|dự báo|mưa|nắng|bão|lũ|động đất|tin tức|báo chí|thời sự", _F),
    re.compile(r"bệnh viện|thuốc|chữa bệnh|khám bệnh|sức khỏe|triệu chứng|bác sĩ ơi|đau đầu|sốt|cảm cúm", _F),
    re.compile(r"nấu ăn|công thức nấu|nguyên liệu nấu|món ăn|thực đơn|ăn gì ngon", _F),
    re.compile(r"phim (?:hay|mới|chiếu)|bài hát|ca sĩ|diễn viên|xem phim|nghe nhạc|game (?:hay|mới)", _F),
    re.compile(
        r"bóng đá|kết quả bóng|đội tuyển|trận đấu|giải đấu|bóng rổ|tennis|cầu lông"
        r"|world cup|worldcup|euro|champions league|ngoại hạng anh|la liga|bundesliga"
        r"|tỉ số|tỷ số|chung kết|vô địch|huy chương|olympic|seagame|sea game"
        r"|cầu thủ|vận động viên|hlv|huấn luyện viên đội",
        _F,
    ),
]

_SAFE_KEYWORDS = re.compile(
    r"ngành|chuyên ngành|môn học|giảng viên|sinh viên|đại học|neu|kinh tế quốc dân"
    r"|chương trình đào tạo|tuyển sinh|điểm chuẩn|nghề nghiệp|kỹ năng|mbti|tính cách",
    _F,
)

OFF_TOPIC_ANSWER = (
    "Câu hỏi này nằm ngoài phạm vi của tôi. Tôi chuyên tư vấn về **ngành học, môn học, "
    "giảng viên và nghề nghiệp** tại NEU.\n\n"
    "Nếu bạn cần hỗ trợ về tuyển sinh, hãy tham khảo 2 agent chuyên biệt:\n"
    "- 📋 **Thông tin tuyển sinh NEU 2026** (quy chế, phương thức, lộ trình, học phí) → "
    "[ai.neu.edu.vn/tuyen-sinh](https://ai.neu.edu.vn/tuyen-sinh/tools/neu-admission-info)\n"
    "- 🔢 **Quy đổi và tư vấn điểm** (IELTS/TOEFL/SAT/HSA/THPT → điểm xét tuyển NEU) → "
    "[ai.neu.edu.vn/quy-doi](https://ai.neu.edu.vn/tuyen-sinh/tools/convertum)\n\n"
    "Tôi có thể giúp bạn về:\n"
    "- 🎓 Ngành học, môn học, chương trình đào tạo tại NEU\n"
    "- 💼 Nghề nghiệp, cơ hội việc làm sau tốt nghiệp\n"
    "- 🧠 Định hướng theo tính cách MBTI\n"
    "- 📊 Điểm chuẩn và chỉ tiêu tuyển sinh từng ngành\n\n"
    "Bạn có muốn hỏi về những chủ đề trên không?"
)


def detect_off_topic(question: str) -> bool:
    if _SAFE_KEYWORDS.search(question or ""):
        return False
    return any(p.search(question or "") for p in _OFF_TOPIC_PATTERNS)


__all__ = [
    "ADMISSION_INFO_ANSWER",
    "CHATBOT_IDENTITY",
    "OFF_TOPIC_ANSWER",
    "SCORE_CONVERT_ANSWER",
    "SELF_INTRO_ANSWER",
    "detect_admission_info",
    "detect_meta_question",
    "detect_off_topic",
    "detect_score_convert",
    "detect_self_intro",
    "detect_tuition_question",
]

