from __future__ import annotations

import re

_F = re.IGNORECASE | re.UNICODE

_PROGRAM_CODE_COMPARE_PATTERN = re.compile(
    r"kh[aá]c\s*nhau|so\s*s[aá]nh|ph[aâ]n\s*bi[eệ]t|ph[aâ]n\s*lo[aạ]i|gi[aả]i\s*th[ií]ch"
    r".{0,60}(m[aã]\s*(?:x[eé]t\s*tuy[eể]n|tuy[eể]n\s*sinh|ch[uơ]ng\s*tr[iì]nh)|"
    r"(?:clc|ti[eê]n\s*ti[eế]n|pohe|epmp|e-?bba|ep\d+|tt\d+)|"
    r"h[eệ]\s*(?:đại\s*trà|ti[eê]u\s*chu[aẩ]n|ch[ií]nh\s*quy|ch[aấ]t\s*l[uợ]ng\s*cao|ti[eê]n\s*ti[eế]n|ti[eế]ng\s*anh|pohe))"
    r"|m[aã]\s*(?:x[eé]t\s*tuy[eể]n|tuy[eể]n\s*sinh).{0,60}kh[aá]c\s*nhau",
    _F,
)

_PROGRAM_TYPE_TABLE: list[dict[str, str]] = [
    {
        "type": "STANDARD",
        "name": "Tiêu chuẩn (Đại trà / Chính quy)",
        "code": "Mã ngành 7 chữ số (VD: 7340101, 7480201)",
        "language": "Tiếng Việt",
        "class_size": "Thường lớn",
        "tuition": "Thấp nhất",
    },
    {
        "type": "CLC",
        "name": "Chất lượng cao (CLC)",
        "code": "CLC1/CLC2/CLC3",
        "language": "Việt + Anh",
        "class_size": "40–60",
        "tuition": "Cao hơn đại trà",
    },
    {
        "type": "TT",
        "name": "Tiên tiến (TT)",
        "code": "TT1/TT2",
        "language": "Gần 100% Tiếng Anh",
        "class_size": "Nhỏ, chọn lọc",
        "tuition": "Rất cao",
    },
    {
        "type": "EP",
        "name": "Tiếng Anh (EP / E-BBA / EPMP)",
        "code": "EPxx / EBBA / EPMP",
        "language": "100% Tiếng Anh",
        "class_size": "Nhỏ đến vừa",
        "tuition": "Cao",
    },
    {
        "type": "POHE",
        "name": "POHE (Định hướng nghề nghiệp)",
        "code": "POHE1–POHE7",
        "language": "Tiếng Việt (thiên thực hành)",
        "class_size": "50–60",
        "tuition": "Tùy chương trình (thường ≥ đại trà)",
    },
]


def handle_program_code_comparison_question(question: str) -> str | None:
    """
    Bắt các câu hỏi so sánh/phân biệt 'mã xét tuyển/mã chương trình' nhưng không nêu rõ
    CLC/TT/EP/POHE... để vẫn trả lời được.
    """
    if not _PROGRAM_CODE_COMPARE_PATTERN.search(question):
        return None

    lines: list[str] = []
    lines.append("### So sánh các loại mã/chương trình đào tạo tại NEU\n")
    lines.append("| Nhóm chương trình | Nhận biết mã | Ngôn ngữ | Quy mô lớp | Học phí |")
    lines.append("|---|---|---|---|---|")
    for row in _PROGRAM_TYPE_TABLE:
        lines.append(
            f"| {row['name']} | {row['code']} | {row['language']} | {row['class_size']} | {row['tuition']} |"
        )
    lines.append(
        "\nBạn có thể xem thêm tại [tuyensinh.neu.edu.vn](https://tuyensinh.neu.edu.vn)."
    )
    return "\n".join(lines)


__all__ = ["handle_program_code_comparison_question"]

