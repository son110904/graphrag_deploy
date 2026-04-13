"""
==========================================================================
FIELD TAXONOMY MODULE — Phân cấp Lĩnh vực → Nhóm ngành → Ngành → Chương trình
Bổ sung vào index.py ngay sau ADMISSION_DATA (~dòng 99)
==========================================================================
Giải quyết: câu hỏi về nhóm ngành / lĩnh vực ("ngành kinh tế",
"nhóm CNTT", "lĩnh vực tài chính"...) thay vì chỉ xử lý tên ngành cụ thể.
==========================================================================
"""

import re

_F = re.IGNORECASE | re.UNICODE

# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 1 — Dữ liệu phân cấp đầy đủ
# ══════════════════════════════════════════════════════════════════════════════

FIELD_TAXONOMY: dict = {
    # ── 722 Nghệ thuật và nhân văn ────────────────────────────────────────────
    "722": {
        "name": "Nghệ thuật và nhân văn",
        "groups": {
            "72202": {
                "name": "Ngôn ngữ",
                "majors": {
                    "7220201": {
                        "name": "Ngôn ngữ Anh",
                        "programs": [
                            {"ten": "Ngôn ngữ Anh", "ma_xt": "7220201"},
                        ],
                    },
                },
            },
        },
    },

    # ── 731 Khoa học xã hội và hành vi ────────────────────────────────────────
    "731": {
        "name": "Khoa học xã hội và hành vi",
        "groups": {
            "73101": {
                "name": "Kinh tế học",
                "majors": {
                    "7310101": {
                        "name": "Kinh tế",
                        "programs": [
                            {"ten": "Kinh tế học",                       "ma_xt": "7310101_1"},
                            {"ten": "Kinh tế và quản lý đô thị",         "ma_xt": "7310101_2"},
                            {"ten": "Kinh tế và quản lý nguồn nhân lực", "ma_xt": "7310101_3"},
                            {"ten": "Kinh tế học tài chính (FE)",         "ma_xt": "EP13"},
                            {"ten": "Quản lý công và chính sách (E-PMP)", "ma_xt": "EPMP"},
                        ],
                    },
                    "7310104": {
                        "name": "Kinh tế đầu tư",
                        "programs": [
                            {"ten": "Kinh tế đầu tư",        "ma_xt": "7310104"},
                            {"ten": "Kinh tế đầu tư (CLC)",  "ma_xt": "CLC2"},
                        ],
                    },
                    "7310105": {
                        "name": "Kinh tế phát triển",
                        "programs": [
                            {"ten": "Kinh tế phát triển",       "ma_xt": "7310105"},
                            {"ten": "Kinh tế phát triển (CLC)", "ma_xt": "CLC1"},
                            {"ten": "Phát triển quốc tế",        "ma_xt": "EP25"},
                        ],
                    },
                    "7310106": {
                        "name": "Kinh tế quốc tế",
                        "programs": [
                            {"ten": "Kinh tế quốc tế",       "ma_xt": "7310106"},
                            {"ten": "Kinh tế quốc tế (CLC)", "ma_xt": "CLC3"},
                            {"ten": "Kinh tế quốc tế (EP)",  "ma_xt": "EP22"},
                        ],
                    },
                    "7310107": {
                        "name": "Thống kê kinh tế",
                        "programs": [
                            {"ten": "Thống kê kinh tế",                    "ma_xt": "7310107"},
                            {"ten": "Thống kê và Trí tuệ kinh doanh (EP)", "ma_xt": "EP32"},
                        ],
                    },
                    "7310108": {
                        "name": "Toán kinh tế",
                        "programs": [
                            {"ten": "Toán kinh tế",                                    "ma_xt": "7310108"},
                            {"ten": "Khoa học tính toán trong Tài chính và Bảo hiểm", "ma_xt": "EP02"},
                            {"ten": "Phân tích dữ liệu kinh tế (EDA)",                "ma_xt": "EP03"},
                            {"ten": "Quản trị rủi ro định lượng",                     "ma_xt": "EP29"},
                        ],
                    },
                    "7310109": {
                        "name": "Kinh tế số",
                        "programs": [
                            {"ten": "Kinh tế số (dự kiến)", "ma_xt": "EP23"},
                        ],
                    },
                },
            },
        },
    },

    # ── 732 Báo chí và thông tin ──────────────────────────────────────────────
    "732": {
        "name": "Báo chí và thông tin",
        "groups": {
            "73201": {
                "name": "Báo chí và truyền thông",
                "majors": {
                    "7320108": {
                        "name": "Quan hệ công chúng",
                        "programs": [
                            {"ten": "Quan hệ công chúng",       "ma_xt": "7320108"},
                            {"ten": "Quan hệ công chúng (CLC)", "ma_xt": "CLC2"},
                        ],
                    },
                },
            },
        },
    },

    # ── 734 Kinh doanh và quản lý ─────────────────────────────────────────────
    "734": {
        "name": "Kinh doanh và quản lý",
        "groups": {
            "73401": {
                "name": "Kinh doanh",
                "majors": {
                    "7340101": {
                        "name": "Quản trị kinh doanh",
                        "programs": [
                            {"ten": "Quản trị kinh doanh",                      "ma_xt": "7340101"},
                            {"ten": "Quản trị kinh doanh (CLC)",                "ma_xt": "CLC2"},
                            {"ten": "Quản trị kinh doanh (E-BBA)",              "ma_xt": "EBBA"},
                            {"ten": "Khởi nghiệp và phát triển kinh doanh",     "ma_xt": "EP01"},
                            {"ten": "Kinh doanh số (E-BDB)",                    "ma_xt": "EP05"},
                            {"ten": "Phân tích kinh doanh (BA)",                "ma_xt": "EP06"},
                            {"ten": "Quản trị điều hành thông minh (E-SOM)",   "ma_xt": "EP07"},
                            {"ten": "Quản trị chất lượng và Đổi mới (E-MQI)",  "ma_xt": "EP08"},
                            {"ten": "Quản trị kinh doanh (TT1)",               "ma_xt": "TT1"},
                        ],
                    },
                    "7340115": {
                        "name": "Marketing",
                        "programs": [
                            {"ten": "Marketing",                "ma_xt": "7340115"},
                            {"ten": "Marketing số (CLC)",       "ma_xt": "CLC3"},
                            {"ten": "Quản trị Marketing (CLC)", "ma_xt": "CLC3"},
                            {"ten": "Truyền thông Marketing",   "ma_xt": "POHE3"},
                            {"ten": "Công nghệ Marketing",      "ma_xt": "EP19"},
                        ],
                    },
                    "7340116": {
                        "name": "Bất động sản",
                        "programs": [
                            {"ten": "Bất động sản", "ma_xt": "7340116"},
                        ],
                    },
                    "7340120": {
                        "name": "Kinh doanh quốc tế",
                        "programs": [
                            {"ten": "Kinh doanh quốc tế",                    "ma_xt": "7340120"},
                            {"ten": "Quản trị Kinh doanh quốc tế (CLC)",     "ma_xt": "CLC3"},
                            {"ten": "Kinh doanh quốc tế (TT2)",              "ma_xt": "TT2"},
                        ],
                    },
                    "7340121": {
                        "name": "Kinh doanh thương mại",
                        "programs": [
                            {"ten": "Kinh doanh thương mại",          "ma_xt": "7340121"},
                            {"ten": "Quản trị kinh doanh thương mại", "ma_xt": "POHE5"},
                            {"ten": "Quản lý thị trường",             "ma_xt": "POHE6"},
                        ],
                    },
                    "7340122": {
                        "name": "Thương mại điện tử",
                        "programs": [
                            {"ten": "Thương mại điện tử",       "ma_xt": "7340122"},
                            {"ten": "Thương mại điện tử (CLC)", "ma_xt": "CLC3"},
                        ],
                    },
                },
            },
            "73402": {
                "name": "Tài chính – Ngân hàng – Bảo hiểm",
                "majors": {
                    "7340201": {
                        "name": "Tài chính Ngân hàng",
                        "programs": [
                            {"ten": "Tài chính – Ngân hàng",                "ma_xt": "7340201"},
                            {"ten": "Ngân hàng (CLC)",                       "ma_xt": "CLC1"},
                            {"ten": "Tài chính doanh nghiệp (CLC)",         "ma_xt": "CLC3"},
                            {"ten": "Công nghệ tài chính và Ngân hàng số",  "ma_xt": "EP09"},
                            {"ten": "Tài chính và Đầu tư (BFI)",            "ma_xt": "EP10"},
                            {"ten": "Thẩm định giá (EP)",                   "ma_xt": "EP31"},
                            {"ten": "Thẩm định giá (POHE)",                 "ma_xt": "POHE7"},
                            {"ten": "Kế hoạch Tài chính (TT1)",             "ma_xt": "TT1"},
                            {"ten": "Tài chính (TT2)",                      "ma_xt": "TT2"},
                        ],
                    },
                    "7340204": {
                        "name": "Bảo hiểm",
                        "programs": [
                            {"ten": "Bảo hiểm",                                     "ma_xt": "7340204"},
                            {"ten": "Bảo hiểm tích hợp chứng chỉ ANZIIF (CLC)",    "ma_xt": "CLC1"},
                        ],
                    },
                    "7340205": {
                        "name": "Công nghệ tài chính",
                        "programs": [
                            {"ten": "Công nghệ tài chính (dự kiến)", "ma_xt": "7340205"},
                        ],
                    },
                },
            },
            "73403": {
                "name": "Kế toán – Kiểm toán",
                "majors": {
                    "7340301": {
                        "name": "Kế toán",
                        "programs": [
                            {"ten": "Kế toán",                                          "ma_xt": "7340301"},
                            {"ten": "Kiểm toán tích hợp chứng chỉ ACCA (CLC)",         "ma_xt": "CLC3"},
                            {"ten": "Kế toán tích hợp chứng chỉ ICAEW CFAB",           "ma_xt": "EP04"},
                            {"ten": "Kế toán (TT1)",                                   "ma_xt": "TT1"},
                        ],
                    },
                    "7340302": {
                        "name": "Kiểm toán",
                        "programs": [
                            {"ten": "Kiểm toán",                                        "ma_xt": "7340302"},
                            {"ten": "Kiểm toán nội bộ",                                "ma_xt": "EP21"},
                            {"ten": "Kiểm toán tích hợp chứng chỉ ICAEW CFAB (CLC)",  "ma_xt": "EP12"},
                        ],
                    },
                },
            },
            "73404": {
                "name": "Quản trị – Quản lý",
                "majors": {
                    "7340401": {
                        "name": "Khoa học quản lý",
                        "programs": [
                            {"ten": "Khoa học quản lý", "ma_xt": "7340401"},
                        ],
                    },
                    "7340403": {
                        "name": "Quản lý công",
                        "programs": [
                            {"ten": "Quản lý công", "ma_xt": "7340403"},
                        ],
                    },
                    "7340404": {
                        "name": "Quản trị nhân lực",
                        "programs": [
                            {"ten": "Quản trị nhân lực",                "ma_xt": "7340404"},
                            {"ten": "Quản trị nhân lực (CLC)",          "ma_xt": "CLC2"},
                            {"ten": "Quản trị nhân lực quốc tế (EP)",   "ma_xt": "EP28"},
                        ],
                    },
                    "7340405": {
                        "name": "Hệ thống thông tin quản lý",
                        "programs": [
                            {"ten": "Hệ thống thông tin quản lý", "ma_xt": "7340405"},
                        ],
                    },
                    "7340408": {
                        "name": "Quan hệ lao động",
                        "programs": [
                            {"ten": "Quan hệ lao động", "ma_xt": "7340408"},
                        ],
                    },
                    "7340409": {
                        "name": "Quản lý dự án",
                        "programs": [
                            {"ten": "Quản lý dự án", "ma_xt": "7340409"},
                        ],
                    },
                },
            },
        },
    },

    # ── 738 Pháp luật ─────────────────────────────────────────────────────────
    "738": {
        "name": "Pháp luật",
        "groups": {
            "73801": {
                "name": "Luật",
                "majors": {
                    "7380101": {
                        "name": "Luật",
                        "programs": [
                            {"ten": "Luật", "ma_xt": "7380101"},
                        ],
                    },
                    "7380107": {
                        "name": "Luật kinh tế",
                        "programs": [
                            {"ten": "Luật kinh tế",  "ma_xt": "7380107"},
                            {"ten": "Luật kinh doanh (POHE)", "ma_xt": "POHE4"},
                        ],
                    },
                    "7380109": {
                        "name": "Luật thương mại quốc tế",
                        "programs": [
                            {"ten": "Luật thương mại quốc tế", "ma_xt": "7380109"},
                        ],
                    },
                },
            },
        },
    },

    # ── 746 Toán và thống kê ──────────────────────────────────────────────────
    "746": {
        "name": "Toán và thống kê",
        "groups": {
            "74601": {
                "name": "Toán và thống kê",
                "majors": {
                    "7460108": {
                        "name": "Khoa học dữ liệu",
                        "programs": [
                            {"ten": "Khoa học dữ liệu (EP15)",                               "ma_xt": "EP15"},
                            {"ten": "Công nghệ Logistics và Quản trị chuỗi cung ứng (EP20)", "ma_xt": "EP20"},
                        ],
                    },
                    "7460112": {
                        "name": "Toán ứng dụng",
                        "programs": [
                            {"ten": "Toán ứng dụng (dự kiến)", "ma_xt": "EP30"},
                        ],
                    },
                },
            },
        },
    },

    # ── 748 Máy tính và công nghệ thông tin ────────────────────────────────────
    "748": {
        "name": "Máy tính và công nghệ thông tin",
        "groups": {
            "74801": {
                "name": "Máy tính và công nghệ thông tin",
                "majors": {
                    "7480101": {
                        "name": "Khoa học máy tính",
                        "programs": [
                            {"ten": "Khoa học máy tính", "ma_xt": "7480101"},
                        ],
                    },
                    "7480103": {
                        "name": "Kỹ thuật phần mềm",
                        "programs": [
                            {"ten": "Kỹ thuật phần mềm (EP17)", "ma_xt": "EP17"},
                        ],
                    },
                    "7480104": {
                        "name": "Hệ thống thông tin",
                        "programs": [
                            {"ten": "Hệ thống thông tin", "ma_xt": "7480104"},
                        ],
                    },
                    "7480107": {
                        "name": "Trí tuệ nhân tạo",
                        "programs": [
                            {"ten": "Trí tuệ nhân tạo (EP16)", "ma_xt": "EP16"},
                        ],
                    },
                    "7480201": {
                        "name": "Công nghệ thông tin",
                        "programs": [
                            {"ten": "Công nghệ thông tin",                      "ma_xt": "7480201"},
                            {"ten": "Công nghệ thông tin và chuyển đổi số (CLC)", "ma_xt": "CLC1"},
                        ],
                    },
                    "7480202": {
                        "name": "An toàn thông tin",
                        "programs": [
                            {"ten": "An toàn thông tin", "ma_xt": "7480202"},
                        ],
                    },
                },
            },
        },
    },

    # ── 751 Công nghệ kỹ thuật ────────────────────────────────────────────────
    "751": {
        "name": "Công nghệ kỹ thuật",
        "groups": {
            "75101": {
                "name": "Công nghệ kỹ thuật",
                "majors": {
                    "7510605": {
                        "name": "Logistics và Quản lý chuỗi cung ứng",
                        "programs": [
                            {"ten": "Logistics và quản lý chuỗi cung ứng",                           "ma_xt": "7510605"},
                            {"ten": "Logistics và quản lý chuỗi cung ứng (CLC)",                     "ma_xt": "CLC3"},
                            {"ten": "Logistics và quản lý CCU tích hợp chứng chỉ quốc tế (LSIC)",   "ma_xt": "EP14"},
                        ],
                    },
                },
            },
        },
    },

    # ── 762 Nông nghiệp ──────────────────────────────────────────────────────
    "762": {
        "name": "Nông nghiệp",
        "groups": {
            "76201": {
                "name": "Nông nghiệp",
                "majors": {
                    "7620114": {
                        "name": "Kinh doanh nông nghiệp",
                        "programs": [
                            {"ten": "Kinh doanh nông nghiệp", "ma_xt": "7620114"},
                        ],
                    },
                    "7620115": {
                        "name": "Kinh tế nông nghiệp",
                        "programs": [
                            {"ten": "Kinh tế nông nghiệp", "ma_xt": "7620115"},
                        ],
                    },
                },
            },
        },
    },

    # ── 781 Du lịch, khách sạn ────────────────────────────────────────────────
    "781": {
        "name": "Du lịch, khách sạn, thể thao và dịch vụ cá nhân",
        "groups": {
            "78101": {
                "name": "Du lịch và khách sạn",
                "majors": {
                    "7810101": {
                        "name": "Du lịch",
                        "programs": [
                            {"ten": "Quản trị giải trí và sự kiện",      "ma_xt": "EP18"},
                            {"ten": "Quản trị công nghiệp sáng tạo",     "ma_xt": "EP27"},
                        ],
                    },
                    "7810103": {
                        "name": "Quản trị dịch vụ du lịch và lữ hành",
                        "programs": [
                            {"ten": "Quản trị dịch vụ du lịch và lữ hành", "ma_xt": "7810103"},
                            {"ten": "Quản trị lữ hành (POHE)",             "ma_xt": "POHE2"},
                        ],
                    },
                    "7810201": {
                        "name": "Quản trị khách sạn",
                        "programs": [
                            {"ten": "Quản trị khách sạn",               "ma_xt": "7810201"},
                            {"ten": "Quản trị khách sạn quốc tế (IHME)", "ma_xt": "EP11"},
                            {"ten": "Quản trị khách sạn (POHE)",         "ma_xt": "POHE1"},
                        ],
                    },
                },
            },
        },
    },

    # ── 785 Tài nguyên và môi trường ─────────────────────────────────────────
    "785": {
        "name": "Tài nguyên và môi trường",
        "groups": {
            "78501": {
                "name": "Tài nguyên và môi trường",
                "majors": {
                    "7850101": {
                        "name": "Quản lý tài nguyên và môi trường",
                        "programs": [
                            {"ten": "Quản lý tài nguyên và môi trường",    "ma_xt": "7850101"},
                            {"ten": "Công nghệ môi trường và phát triển bền vững", "ma_xt": "EP26"},
                        ],
                    },
                    "7850102": {
                        "name": "Kinh tế tài nguyên thiên nhiên",
                        "programs": [
                            {"ten": "Kinh tế tài nguyên thiên nhiên", "ma_xt": "7850102"},
                            {"ten": "Kinh tế Y tế",                   "ma_xt": "EP24"},
                        ],
                    },
                    "7850103": {
                        "name": "Quản lý đất đai",
                        "programs": [
                            {"ten": "Quản lý đất đai", "ma_xt": "7850103"},
                        ],
                    },
                },
            },
        },
    },
}


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 2 — Lookup tables phẳng (tính một lần khi load)
# ══════════════════════════════════════════════════════════════════════════════

# ma_nganh → {"field_code", "field_name", "group_code", "group_name", "major_name"}
_MAJOR_TO_CONTEXT: dict[str, dict] = {}

# ma_xt (admission code) → {"field_code", "group_code", "ma_nganh", ...}
_MA_XT_TO_CONTEXT: dict[str, dict] = {}

# flat list of all programs for quick search
_ALL_PROGRAMS_FLAT: list[dict] = []


def _build_lookup_tables() -> None:
    """Xây dựng lookup tables từ FIELD_TAXONOMY (gọi 1 lần khi module load)."""
    for field_code, field_data in FIELD_TAXONOMY.items():
        field_name = field_data["name"]
        for group_code, group_data in field_data.get("groups", {}).items():
            group_name = group_data["name"]
            for ma_nganh, major_data in group_data.get("majors", {}).items():
                major_name = major_data["name"]
                ctx = {
                    "field_code":  field_code,
                    "field_name":  field_name,
                    "group_code":  group_code,
                    "group_name":  group_name,
                    "ma_nganh":    ma_nganh,
                    "major_name":  major_name,
                }
                _MAJOR_TO_CONTEXT[ma_nganh] = ctx
                for prog in major_data.get("programs", []):
                    ma_xt = prog.get("ma_xt", "")
                    prog_ctx = {**ctx, "ten_chuong_trinh": prog["ten"], "ma_xt": ma_xt}
                    _MA_XT_TO_CONTEXT[ma_xt.upper()] = prog_ctx
                    _ALL_PROGRAMS_FLAT.append(prog_ctx)


_build_lookup_tables()


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 3 — Từ điển đồng nghĩa cho lĩnh vực / nhóm ngành
# ══════════════════════════════════════════════════════════════════════════════

# Pattern → field_code (tìm theo lĩnh vực)
_FIELD_SYNONYMS: list[tuple[re.Pattern, str]] = [
    # 722
    (re.compile(r"ngo[aạ]i\s*ng[ữu]|ng[oô]n\s*ng[ữu]\s*anh|ti[eế]ng\s*anh(?!\s*(?:clc|ep|tt|chương))", _F), "722"),
    # 731
    (re.compile(r"kinh\s*t[eế]\s*h[oọ]c|l[iĩ]nh\s*v[uự]c\s*kinh\s*t[eế](?!\s*(?:qu[oố]c\s*t[eế]|đ[aầ]u\s*t[uư]))", _F), "731"),
    # 732
    (re.compile(r"b[aá]o\s*ch[ií]|truy[eề]n\s*th[oô]ng|th[oô]ng\s*tin\s*(?:đ[aạ]i\s*ch[uú]ng|b[aá]o\s*ch[ií])", _F), "732"),
    # 734 (rộng)
    (re.compile(r"kinh\s*doanh\s*v[aà]\s*qu[aả]n\s*l[ýy]|l[iĩ]nh\s*v[uự]c\s*qu[aả]n\s*tr[ịi]", _F), "734"),
    # 738
    (re.compile(r"ph[aá]p\s*lu[aậ]t|lu[aậ]t\s*kinh\s*t[eế]|lu[aậ]t(?:\s*th[uư][oơ]ng\s*m[aạ]i)?", _F), "738"),
    # 746
    (re.compile(r"to[aá]n\s*(?:v[aà]\s*)?th[oố]ng\s*k[eê]|to[aá]n\s*[uứ]ng\s*d[uụ]ng", _F), "746"),
    # 748
    (re.compile(r"(?:m[aá]y\s*t[ií]nh|cntt|c[oô]ng\s*ngh[eệ]\s*th[oô]ng\s*tin|it\b|khoa\s*h[oọ]c\s*m[aá]y\s*t[ií]nh)", _F), "748"),
    # 751
    (re.compile(r"logistics|chu[oỗ]i\s*cung\s*[uứ]ng|c[oô]ng\s*ngh[eệ]\s*k[ỹy]\s*thu[aậ]t", _F), "751"),
    # 762
    (re.compile(r"n[oô]ng\s*nghi[eệ]p|kinh\s*doanh\s*n[oô]ng\s*nghi[eệ]p|kinh\s*t[eế]\s*n[oô]ng", _F), "762"),
    # 781
    (re.compile(r"du\s*l[iị]ch|kh[aá]ch\s*s[aạ]n|l[ữu]\s*h[aà]nh|gi[aả]i\s*tr[ií]", _F), "781"),
    # 785
    (re.compile(r"t[aà]i\s*nguy[eê]n|m[oô]i\s*tr[uư][oờ]ng|[dđ][aấ]t\s*[dđ]ai", _F), "785"),
]

# Pattern → group_code (tìm theo nhóm ngành chính xác hơn)
_GROUP_SYNONYMS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"kinh\s*t[eế]\s*h[oọ]c(?!\s*t[aà]i\s*ch[ií]nh)|nh[oó]m\s*kinh\s*t[eế]\s*h[oọ]c", _F), "73101"),
    (re.compile(r"t[aà]i\s*ch[ií]nh\s*ng[aâ]n\s*h[aà]ng\s*b[aả]o\s*hi[eể]m|nh[oó]m\s*t[aà]i\s*ch[ií]nh", _F), "73402"),
    (re.compile(r"k[eế]\s*to[aá]n\s*ki[eể]m\s*to[aá]n|nh[oó]m\s*k[eế]\s*to[aá]n", _F), "73403"),
    (re.compile(r"qu[aả]n\s*tr[ịi]\s*qu[aả]n\s*l[ýy]|nh[oó]m\s*qu[aả]n\s*tr[ịi]", _F), "73404"),
    (re.compile(r"kinh\s*doanh(?!\s*(?:qu[oố]c\s*t[eế]|th[uư][oơ]ng\s*m[aạ]i))|nh[oó]m\s*kinh\s*doanh", _F), "73401"),
    (re.compile(r"lu[aậ]t(?!\s*kinh\s*t[eế])|nh[oó]m\s*lu[aậ]t", _F), "73801"),
]


def _find_field_code(question: str) -> str | None:
    """Trả về field_code khớp đầu tiên trong câu hỏi, hoặc None."""
    for pattern, code in _FIELD_SYNONYMS:
        if pattern.search(question):
            return code
    return None


def _find_group_code(question: str) -> str | None:
    """Trả về group_code khớp đầu tiên, hoặc None."""
    for pattern, code in _GROUP_SYNONYMS:
        if pattern.search(question):
            return code
    return None


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 4 — Helper: lấy programs theo lĩnh vực / nhóm / ngành
# ══════════════════════════════════════════════════════════════════════════════

def get_context_for_major(ma_nganh: str) -> dict | None:
    """Trả về {field_code, field_name, group_code, group_name, major_name} cho 1 mã ngành."""
    return _MAJOR_TO_CONTEXT.get(ma_nganh)


def get_context_for_admission_code(ma_xt: str) -> dict | None:
    """Trả về context đầy đủ từ mã xét tuyển."""
    return _MA_XT_TO_CONTEXT.get(ma_xt.upper())


def find_programs_by_field(field_code: str) -> list[dict]:
    """Lấy toàn bộ programs thuộc một lĩnh vực (field_code)."""
    return [p for p in _ALL_PROGRAMS_FLAT if p["field_code"] == field_code]


def find_programs_by_group(group_code: str) -> list[dict]:
    """Lấy toàn bộ programs thuộc một nhóm ngành (group_code)."""
    return [p for p in _ALL_PROGRAMS_FLAT if p["group_code"] == group_code]


def find_programs_by_major(ma_nganh: str) -> list[dict]:
    """Lấy toàn bộ programs thuộc một mã ngành."""
    return [p for p in _ALL_PROGRAMS_FLAT if p["ma_nganh"] == ma_nganh]


def enrich_admission_entry_with_taxonomy(entry: dict) -> dict:
    """
    Thêm field/group context vào 1 entry của ADMISSION_DATA.
    Dùng khi build câu trả lời cần hiển thị 'lĩnh vực: ..., nhóm ngành: ...'.
    """
    ma_nganh = entry.get("ma_nganh", "")
    ctx = _MAJOR_TO_CONTEXT.get(ma_nganh)
    if ctx:
        return {**entry, **{k: v for k, v in ctx.items() if k not in entry}}
    return entry


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 5 — Pattern nhận diện câu hỏi về lĩnh vực / nhóm ngành
# ══════════════════════════════════════════════════════════════════════════════

_FIELD_QUESTION_PATTERN = re.compile(
    # Câu hỏi liệt kê ngành trong lĩnh vực
    r"(?:c[aá]c\s*ng[àa]nh|ng[àa]nh\s*n[àa]o|nh[oó]m\s*ng[àa]nh|danh\s*s[aá]ch\s*ng[àa]nh)"
    r".{0,30}"
    r"(?:thu[oộ]c|trong|c[uủ]a|l[iĩ]nh\s*v[uự]c|nh[oó]m)"
    # Câu hỏi về lĩnh vực cụ thể
    r"|l[iĩ]nh\s*v[uự]c\s*(?:kinh\s*t[eế]|cntt|c[oô]ng\s*ngh[eệ]|t[aà]i\s*ch[ií]nh|lu[aậ]t|du\s*l[iị]ch|n[oô]ng\s*nghi[eệ]p)"
    # Hỏi thẳng "NEU có ngành IT không"
    r"|(?:neu|tr[uư][oờ]ng).{0,20}(?:c[oó]\s*ng[àa]nh|[dđ][aà]o\s*t[aạ]o).{0,30}"
    r"(?:cntt|it\b|m[aá]y\s*t[ií]nh|c[oô]ng\s*ngh[eệ]|t[aà]i\s*ch[ií]nh|lu[aậ]t|kinh\s*t[eế])",
    _F,
)

# Câu hỏi "NEU có ngành X không" / "ngành X ở NEU" → tìm theo tên ngành trong taxonomy
_MAJOR_EXIST_PATTERN = re.compile(
    r"(?:neu|tr[uư][oờ]ng).{0,15}c[oó]\s*ng[àa]nh"
    r"|ng[àa]nh.{0,15}(?:neu|tr[uư][oờ]ng|[oở]\s*(?:neu|tr[uư][oờ]ng))"
    r"|(?:c[oó]|t[uồ]n\s*t[aạ]i|[dđ][aà]o\s*t[aạ]o).{0,20}ng[àa]nh",
    _F,
)


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 6 — Format câu trả lời về lĩnh vực / nhóm ngành
# ══════════════════════════════════════════════════════════════════════════════

def format_field_answer(field_code: str | None, group_code: str | None, question: str) -> str:
    """
    Build câu trả lời liệt kê ngành theo lĩnh vực hoặc nhóm ngành.
    Ưu tiên group nếu có; fallback sang field.
    """
    if group_code:
        programs = find_programs_by_group(group_code)
        # Tìm tên nhóm
        group_name = ""
        for fdata in FIELD_TAXONOMY.values():
            if group_code in fdata.get("groups", {}):
                group_name = fdata["groups"][group_code]["name"]
                break
        scope_label = f"nhóm ngành **{group_name}**" if group_name else f"nhóm {group_code}"
    elif field_code:
        programs = find_programs_by_field(field_code)
        field_name = FIELD_TAXONOMY.get(field_code, {}).get("name", field_code)
        scope_label = f"lĩnh vực **{field_name}**"
    else:
        return ""

    if not programs:
        return f"Hiện chưa có dữ liệu ngành cho {scope_label} tại NEU."

    # Nhóm theo ma_nganh để không lặp lại tên ngành
    from collections import defaultdict as _dd
    by_major: dict[str, list] = _dd(list)
    major_names: dict[str, str] = {}
    for p in programs:
        by_major[p["ma_nganh"]].append(p)
        major_names[p["ma_nganh"]] = p["major_name"]

    lines = [f"NEU đào tạo các ngành trong {scope_label}:\n"]
    for ma_nganh, progs in by_major.items():
        major_name = major_names[ma_nganh]
        lines.append(f"**{major_name}** (mã {ma_nganh})")
        for p in progs:
            # Xác định loại chương trình từ ma_xt
            # (gọi _classify_program_type nếu đã import, hoặc inline)
            ma_xt = p["ma_xt"]
            ptype_map = {
                "CLC": "🔵 CLC",
                "TT": "🟣 Tiên tiến",
                "EP": "🟢 EP/Tiếng Anh",
                "POHE": "🟡 POHE",
                "STANDARD": "⚪ Chính quy",
            }
            # Simple inline classify
            mxt_up = ma_xt.upper()
            if mxt_up.startswith("CLC"):
                ptype = "🔵 CLC"
            elif mxt_up.startswith("TT"):
                ptype = "🟣 Tiên tiến"
            elif mxt_up.startswith("EP") or mxt_up.startswith("EBBA") or mxt_up.startswith("EPMP"):
                ptype = "🟢 EP"
            elif mxt_up.startswith("POHE"):
                ptype = "🟡 POHE"
            else:
                ptype = "⚪ Chính quy"

            lines.append(f"  • {p['ten_chuong_trinh']} ({ptype} — mã XT: {ma_xt})")
        lines.append("")  # dòng trống phân cách

    total = sum(len(v) for v in by_major.values())
    lines.append(
        f"*(Tổng cộng {len(by_major)} ngành với {total} chương trình đào tạo)*\n\n"
        "💡 Hỏi thêm về điểm chuẩn, chỉ tiêu, hoặc đặc điểm từng chương trình nhé!"
    )
    return "\n".join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 7 — Handler chính: handle_field_question()
# Tích hợp vào kg_ask() TRƯỚC handle_admission_question
# ══════════════════════════════════════════════════════════════════════════════

def handle_field_question(question: str) -> str | None:
    """
    Nếu câu hỏi hỏi về lĩnh vực / nhóm ngành (không phải tên ngành cụ thể)
    → trả về answer string liệt kê ngành.
    Ngược lại → None để pipeline tiếp tục.

    Kích hoạt khi:
      - Có tín hiệu "lĩnh vực X" / "nhóm ngành X" / "ngành IT ở NEU"...
      - Có field_code hoặc group_code khớp từ synonym
    """
    if not _FIELD_QUESTION_PATTERN.search(question) and not _MAJOR_EXIST_PATTERN.search(question):
        return None

    # Thử tìm group (chi tiết hơn) trước
    group_code = _find_group_code(question)
    if group_code:
        return format_field_answer(None, group_code, question)

    # Thử tìm field
    field_code = _find_field_code(question)
    if field_code:
        return format_field_answer(field_code, None, question)

    return None  # Không match → để pipeline xử lý


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 8 — Bổ sung vào extract_query_intent: taxonomy context
# Thêm vào system_msg trong extract_query_intent (~dòng 1472)
# ══════════════════════════════════════════════════════════════════════════════

_INTENT_TAXONOMY_HINT = (
    "Phân cấp đào tạo tại NEU (dùng để xác định keywords chính xác):\n"
    "  Lĩnh vực → Nhóm ngành → Ngành (mã 7 số) → Chương trình (mã xét tuyển)\n"
    "  VD: 'Tài chính' → nhóm 73402 → ngành 7340201 (Tài chính Ngân hàng) → CLC3/EP09/TT2...\n"
    "  VD: 'IT / CNTT' → lĩnh vực 748 → ngành 7480201, 7480103 (EP17), 7480107 (EP16)...\n"
    "Nếu câu hỏi nhắc lĩnh vực / nhóm ngành → đưa TÊN LĨNH VỰC vào keywords, "
    "không chỉ tên ngành đơn lẻ."
)

# Thêm _INTENT_TAXONOMY_HINT vào cuối system_msg trong extract_query_intent


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 9 — Bổ sung vào _MAJOR_SYNONYMS: synonym theo nhóm ngành
# Thêm vào cuối list _MAJOR_SYNONYMS (~dòng 130)
# ══════════════════════════════════════════════════════════════════════════════

_MAJOR_SYNONYMS_TAXONOMY_ADDITIONS: list[tuple] = [
    # Nhóm tài chính rộng
    (re.compile(r"nh[oó]m\s*t[aà]i\s*ch[ií]nh|ng[àa]nh\s*t[aà]i\s*ch[ií]nh(?!\s*ng[aâ]n\s*h[aà]ng)", _F),
     "tài chính ngân hàng"),
    # Nhóm kế toán - kiểm toán
    (re.compile(r"nh[oó]m\s*k[eế]\s*to[aá]n|ng[àa]nh\s*k[eế]\s*to[aá]n\s*ki[eể]m\s*to[aá]n", _F),
     "kế toán"),
    # Nhóm quản trị rộng
    (re.compile(r"nh[oó]m\s*qu[aả]n\s*tr[ịi]|qu[aả]n\s*tr[ịi]\s*qu[aả]n\s*l[ýy]", _F),
     "quản trị kinh doanh"),
    # CNTT / IT
    (re.compile(r"\bcntt\b|\bit\b|m[aá]y\s*t[ií]nh(?!\s*khoa\s*h[oọ]c)", _F),
     "công nghệ thông tin"),
    # Khoa học dữ liệu / AI / ML
    (re.compile(r"data\s*science|khdt|khoa\s*h[oọ]c\s*d[uữ]\s*li[eệ]u", _F),
     "khoa học dữ liệu"),
    # Logistics
    (re.compile(r"logistics|chu[oỗ]i\s*cung\s*[uứ]ng|scm\b", _F),
     "logistics và quản lý chuỗi cung ứng"),
    # Du lịch
    (re.compile(r"du\s*l[iị]ch|kh[aá]ch\s*s[aạ]n|nh[àa]\s*h[aà]ng\b", _F),
     "quản trị khách sạn"),
    # Môi trường
    (re.compile(r"m[oô]i\s*tr[uư][oờ]ng|b[eề]n\s*v[uữ]ng|bi[eế]n\s*[dđ][oổ]i\s*kh[ií]\s*h[aậ]u", _F),
     "quản lý tài nguyên và môi trường"),
    # Nông nghiệp
    (re.compile(r"kinh\s*t[eế]\s*n[oô]ng\s*nghi[eệ]p|n[oô]ng\s*nghi[eệ]p", _F),
     "kinh tế nông nghiệp"),
]


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 10 — Vị trí tích hợp vào kg_ask / /ask endpoint
# ══════════════════════════════════════════════════════════════════════════════

"""
Trong kg_ask(), thêm block này TRƯỚC handle_admission_question:

    # ── Bước 0-pre: Field/Group taxonomy lookup ──────────────────────────
    field_answer = handle_field_question(question)
    if field_answer is not None:
        print(f"\\nA (field): {field_answer[:80]}...")
        return _build_record(
            query_id, question, field_answer, [],
            {"asked_label": "MAJOR", "mentioned_labels": [],
             "keywords": [], "negated_keywords": [],
             "community_id": "FIELD_TAXONOMY"},
            [], [], "field_taxonomy_lookup",
        )

Trong /ask endpoint (~dòng 3317), thêm TRƯỚC handle_admission_question:

    field_answer = handle_field_question(question)
    if field_answer is not None:
        return JSONResponse(
            content={
                "session_id":       session_id,
                "status":           "success",
                "content_markdown": field_answer,
                "debug": {
                    "query_id":   "field_taxonomy",
                    "keywords":   [],
                    "intent":     {"asked_label": "MAJOR"},
                    "node_count": 0,
                },
            },
            headers=CORS_HEADERS,
        )

Trong enrich_admission_entry_with_taxonomy() (đã có ở Block 4), gọi khi
format_admission_answer() cần hiển thị ngữ cảnh lĩnh vực:

    enriched = enrich_admission_entry_with_taxonomy(p)
    field_name = enriched.get("field_name", "")
    group_name = enriched.get("group_name", "")
    # → dùng để thêm dòng "Thuộc: Lĩnh vực Kinh doanh và quản lý > Tài chính – Ngân hàng – Bảo hiểm"
"""


# ══════════════════════════════════════════════════════════════════════════════
# BLOCK 11 — Utility: tra ngược (admission entry → taxonomy context)
# Dùng trong format_admission_answer hoặc generate_answer hints
# ══════════════════════════════════════════════════════════════════════════════

def get_taxonomy_breadcrumb(ma_nganh: str, ma_xt: str = "") -> str:
    """
    Trả về chuỗi breadcrumb phân cấp cho 1 chương trình.
    VD: "Kinh doanh và quản lý > Tài chính – Ngân hàng – Bảo hiểm > Tài chính Ngân hàng"
    """
    ctx = _MAJOR_TO_CONTEXT.get(ma_nganh)
    if not ctx:
        return ""
    return (
        f"{ctx['field_name']} (Lĩnh vực {ctx['field_code']}) "
        f"› {ctx['group_name']} "
        f"› {ctx['major_name']} ({ma_nganh})"
    )


def search_taxonomy_by_name(term: str) -> list[dict]:
    """
    Tìm kiếm chương trình theo tên (substring) trong toàn bộ taxonomy.
    Trả về list prog_ctx có thêm key 'ten_chuong_trinh' và 'ma_xt'.
    Hữu ích khi ADMISSION_DATA fallback không tìm được.
    """
    term_lower = term.lower()
    results = []
    seen = set()
    for prog in _ALL_PROGRAMS_FLAT:
        score = 0
        if term_lower in prog["ten_chuong_trinh"].lower():
            score += 3
        if term_lower in prog["major_name"].lower():
            score += 2
        if term_lower in prog["group_name"].lower():
            score += 1
        if score > 0:
            key = (prog["ma_nganh"], prog["ma_xt"])
            if key not in seen:
                seen.add(key)
                results.append({**prog, "_score": score})
    return sorted(results, key=lambda x: -x["_score"])


# ══════════════════════════════════════════════════════════════════════════════
# TÓM TẮT CÁC VỊ TRÍ CHÈN
# ══════════════════════════════════════════════════════════════════════════════
"""
1. Sau ADMISSION_DATA (~dòng 99):
   → Chèn toàn bộ file này (BLOCK 1–11)

2. _MAJOR_SYNONYMS (~dòng 115):
   → Thêm _MAJOR_SYNONYMS_TAXONOMY_ADDITIONS vào cuối list

3. handle_admission_question (~dòng 404, trong kg_ask ~dòng 3046):
   → Thêm handle_field_question() call TRƯỚC

4. /ask endpoint (~dòng 3317):
   → Thêm field_answer check TRƯỚC admission_answer check

5. extract_query_intent (~dòng 1472):
   → Thêm _INTENT_TAXONOMY_HINT vào cuối system_msg

6. format_admission_answer (tùy chọn):
   → Gọi get_taxonomy_breadcrumb() để thêm dòng "Thuộc lĩnh vực..."

LUỒNG XỬ LÝ MỚI:
  question
    → handle_field_question()         ← Lĩnh vực/nhóm ngành → liệt kê
    → handle_admission_question()     ← Điểm chuẩn/chỉ tiêu cụ thể
    → kg_ask pipeline bình thường
"""