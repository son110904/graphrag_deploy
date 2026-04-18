from __future__ import annotations

import re

from .field_taxonomy import _MAJOR_SYNONYMS_TAXONOMY_ADDITIONS

_F = re.IGNORECASE | re.UNICODE


ADMISSION_DATA: list[dict] = [
    # ── Chương trình Đặc biệt (EP) ─────────────────────────────────────────
    {"so": 1,  "ten_chuong_trinh": "Công nghệ Marketing",              "ma_xet_tuyen": "EP19",      "ma_nganh": "7340115", "ten_nganh": "Marketing",                              "khoa_vien": "Khoa Marketing",                                  "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 2,  "ten_chuong_trinh": "Công nghệ Logistics và Quản trị chuỗi cung ứng", "ma_xet_tuyen": "EP20", "ma_nganh": "7460108", "ten_nganh": "Khoa học dữ liệu",            "khoa_vien": "Khoa Khoa học dữ liệu và Trí tuệ nhân tạo",         "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 3,  "ten_chuong_trinh": "Kiểm toán nội bộ",                 "ma_xet_tuyen": "EP21",      "ma_nganh": "7340302", "ten_nganh": "Kiểm toán",                              "khoa_vien": "Viện Kế toán - Kiểm toán",                        "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 4,  "ten_chuong_trinh": "Kinh tế quốc tế (EP)",             "ma_xet_tuyen": "EP22",      "ma_nganh": "7310106", "ten_nganh": "Kinh tế quốc tế",                        "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",              "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 5,  "ten_chuong_trinh": "Kinh tế Y tế",                     "ma_xet_tuyen": "EP24",      "ma_nganh": "7310101", "ten_nganh": "Kinh tế",                                "khoa_vien": "Khoa Kinh tế học",                                "chi_tieu": 40,  "diem_chuan_2025": None},
    {"so": 6,  "ten_chuong_trinh": "Phát triển quốc tế",               "ma_xet_tuyen": "EP25",      "ma_nganh": "7310105", "ten_nganh": "Kinh tế phát triển",                     "khoa_vien": "Khoa Kế hoạch và Phát triển",                     "chi_tieu": 40,  "diem_chuan_2025": None},
    {"so": 7,  "ten_chuong_trinh": "Công nghệ môi trường và phát triển bền vững", "ma_xet_tuyen": "EP26", "ma_nganh": "7310101", "ten_nganh": "Kinh tế",                         "khoa_vien": "Khoa Môi trường, Biến đổi khí hậu và Đô thị",     "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 8,  "ten_chuong_trinh": "Quản trị công nghiệp sáng tạo",    "ma_xet_tuyen": "EP27",      "ma_nganh": "7810101", "ten_nganh": "Du lịch",                                "khoa_vien": "Khoa Du lịch và Khách sạn",                       "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 9,  "ten_chuong_trinh": "Quản trị nhân lực quốc tế",        "ma_xet_tuyen": "EP28",      "ma_nganh": "7340404", "ten_nganh": "Quản trị nhân lực",                      "khoa_vien": "Khoa Kinh tế và Quản lý nguồn nhân lực",          "chi_tieu": 40,  "diem_chuan_2025": None},
    {"so": 10, "ten_chuong_trinh": "Quản trị rủi ro định lượng",        "ma_xet_tuyen": "EP29",      "ma_nganh": "7310108", "ten_nganh": "Toán kinh tế",                           "khoa_vien": "Khoa Toán kinh tế",                               "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 11, "ten_chuong_trinh": "Thẩm định giá (EP)",                "ma_xet_tuyen": "EP31",      "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                      "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 12, "ten_chuong_trinh": "Thống kê và Trí tuệ kinh doanh",   "ma_xet_tuyen": "EP32",      "ma_nganh": "7310107", "ten_nganh": "Thống kê kinh tế",                       "khoa_vien": "Khoa Thống kê",                                   "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 13, "ten_chuong_trinh": "Kinh tế số (dự kiến)",              "ma_xet_tuyen": "EP23",      "ma_nganh": "7310109", "ten_nganh": "Kinh tế số",                             "khoa_vien": "Khoa Hệ thống thông tin quản lý",                 "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 14, "ten_chuong_trinh": "Toán ứng dụng (dự kiến)",           "ma_xet_tuyen": "EP30",      "ma_nganh": "7460112", "ten_nganh": "Toán ứng dụng",                          "khoa_vien": "Khoa Khoa học Cơ sở",                             "chi_tieu": 50,  "diem_chuan_2025": None},
    {"so": 15, "ten_chuong_trinh": "Công nghệ tài chính (dự kiến)",     "ma_xet_tuyen": "7340205",   "ma_nganh": "7340205", "ten_nganh": "Công nghệ tài chính",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                      "chi_tieu": 50,  "diem_chuan_2025": None},
    # ── POHE ───────────────────────────────────────────────────────────────
    {"so": 16, "ten_chuong_trinh": "Quản trị khách sạn (POHE)",         "ma_xet_tuyen": "POHE1",     "ma_nganh": "7810201", "ten_nganh": "Quản trị khách sạn",                     "khoa_vien": "Khoa Du lịch và Khách sạn",                       "chi_tieu": 50,  "diem_chuan_2025": 25.61},
    {"so": 17, "ten_chuong_trinh": "Quản trị lữ hành (POHE)",           "ma_xet_tuyen": "POHE2",     "ma_nganh": "7810103", "ten_nganh": "Quản trị dịch vụ du lịch và lữ hành",    "khoa_vien": "Khoa Du lịch và Khách sạn",                       "chi_tieu": 50,  "diem_chuan_2025": 24.64},
    {"so": 18, "ten_chuong_trinh": "Truyền thông Marketing (POHE)",     "ma_xet_tuyen": "POHE3",     "ma_nganh": "7340115", "ten_nganh": "Marketing",                              "khoa_vien": "Khoa Marketing",                                  "chi_tieu": 60,  "diem_chuan_2025": 27.61},
    {"so": 19, "ten_chuong_trinh": "Luật kinh doanh (POHE)",            "ma_xet_tuyen": "POHE4",     "ma_nganh": "7380107", "ten_nganh": "Luật kinh tế",                           "khoa_vien": "Khoa Luật",                                       "chi_tieu": 50,  "diem_chuan_2025": 25.5},
    {"so": 20, "ten_chuong_trinh": "Quản trị kinh doanh thương mại (POHE)", "ma_xet_tuyen": "POHE5", "ma_nganh": "7340121", "ten_nganh": "Kinh doanh thương mại",                 "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",              "chi_tieu": 50,  "diem_chuan_2025": 26.29},
    {"so": 21, "ten_chuong_trinh": "Quản lý thị trường (POHE)",         "ma_xet_tuyen": "POHE6",     "ma_nganh": "7340121", "ten_nganh": "Kinh doanh thương mại",                  "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",              "chi_tieu": 50,  "diem_chuan_2025": 24.66},
    {"so": 22, "ten_chuong_trinh": "Thẩm định giá (POHE)",              "ma_xet_tuyen": "POHE7",     "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                      "chi_tieu": 50,  "diem_chuan_2025": 24.55},
    # ── E-BBA / EP01-EP18 ──────────────────────────────────────────────────
    {"so": 23, "ten_chuong_trinh": "Quản trị kinh doanh (E-BBA)",       "ma_xet_tuyen": "EBBA",      "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                    "khoa_vien": "Viện Quản trị Kinh doanh",                        "chi_tieu": 110, "diem_chuan_2025": 25.64},
    {"so": 24, "ten_chuong_trinh": "Khởi nghiệp và phát triển kinh doanh (BBAE)", "ma_xet_tuyen": "EP01", "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",              "khoa_vien": "Viện Đào tạo Quốc tế",                            "chi_tieu": 90,  "diem_chuan_2025": 24.92},
    {"so": 25, "ten_chuong_trinh": "Khoa học tính toán trong Tài chính và Bảo hiểm", "ma_xet_tuyen": "EP02", "ma_nganh": "7310108", "ten_nganh": "Toán kinh tế",               "khoa_vien": "Khoa Toán kinh tế",                               "chi_tieu": 50,  "diem_chuan_2025": 25.5},
    {"so": 26, "ten_chuong_trinh": "Phân tích dữ liệu kinh tế (EDA)",   "ma_xet_tuyen": "EP03",      "ma_nganh": "7310108", "ten_nganh": "Toán kinh tế",                           "khoa_vien": "Khoa Toán kinh tế",                               "chi_tieu": 90,  "diem_chuan_2025": 26.78},
    {"so": 27, "ten_chuong_trinh": "Kế toán tích hợp chứng chỉ quốc tế (ICAEW CFAB)", "ma_xet_tuyen": "EP04", "ma_nganh": "7340301", "ten_nganh": "Kế toán",               "khoa_vien": "Viện Kế toán - Kiểm toán",                        "chi_tieu": 60,  "diem_chuan_2025": 25.9},
    {"so": 28, "ten_chuong_trinh": "Kinh doanh số (E-BDB)",              "ma_xet_tuyen": "EP05",      "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                    "khoa_vien": "Viện Quản trị Kinh doanh",                        "chi_tieu": 60,  "diem_chuan_2025": 26.4},
    {"so": 29, "ten_chuong_trinh": "Phân tích kinh doanh (BA)",          "ma_xet_tuyen": "EP06",      "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                    "khoa_vien": "Viện Đào tạo Tiên tiến, Chất lượng cao và POHE",  "chi_tieu": 60,  "diem_chuan_2025": 27.5},
    {"so": 30, "ten_chuong_trinh": "Quản trị điều hành thông minh (E-SOM)", "ma_xet_tuyen": "EP07",  "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                    "khoa_vien": "Khoa Quản trị kinh doanh",                        "chi_tieu": 70,  "diem_chuan_2025": 25.1},
    {"so": 31, "ten_chuong_trinh": "Quản trị chất lượng và Đổi mới (E-MQI)", "ma_xet_tuyen": "EP08", "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                   "khoa_vien": "Khoa Quản trị kinh doanh",                        "chi_tieu": 70,  "diem_chuan_2025": 24.2},
    {"so": 32, "ten_chuong_trinh": "Công nghệ tài chính và Ngân hàng số", "ma_xet_tuyen": "EP09",    "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                      "chi_tieu": 100, "diem_chuan_2025": 26.29},
    {"so": 33, "ten_chuong_trinh": "Tài chính và Đầu tư (BFI)",          "ma_xet_tuyen": "EP10",      "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                      "chi_tieu": 100, "diem_chuan_2025": 26.27},
    {"so": 34, "ten_chuong_trinh": "Quản trị khách sạn quốc tế (IHME)", "ma_xet_tuyen": "EP11",      "ma_nganh": "7810201", "ten_nganh": "Quản trị khách sạn",                     "khoa_vien": "Khoa Du lịch và Khách sạn",                       "chi_tieu": 50,  "diem_chuan_2025": 24.25},
    {"so": 35, "ten_chuong_trinh": "Kiểm toán tích hợp chứng chỉ quốc tế (ICAEW CFAB)", "ma_xet_tuyen": "EP12", "ma_nganh": "7340302", "ten_nganh": "Kiểm toán",            "khoa_vien": "Viện Kế toán - Kiểm toán",                        "chi_tieu": 60,  "diem_chuan_2025": 27.25},
    {"so": 36, "ten_chuong_trinh": "Kinh tế học tài chính (FE)",         "ma_xet_tuyen": "EP13",      "ma_nganh": "7310101", "ten_nganh": "Kinh tế",                                "khoa_vien": "Khoa Kinh tế học",                                "chi_tieu": 90,  "diem_chuan_2025": 25.41},
    {"so": 37, "ten_chuong_trinh": "Logistics và Quản lý CCU tích hợp chứng chỉ Logistics quốc tế (LSIC)", "ma_xet_tuyen": "EP14", "ma_nganh": "7510605", "ten_nganh": "Logistics và Quản lý chuỗi cung ứng", "khoa_vien": "Viện Thương mại và Kinh tế quốc tế", "chi_tieu": 100, "diem_chuan_2025": 27.69},
    {"so": 38, "ten_chuong_trinh": "Khoa học dữ liệu (EP15)",            "ma_xet_tuyen": "EP15",      "ma_nganh": "7460108", "ten_nganh": "Khoa học dữ liệu",                       "khoa_vien": "Khoa Khoa học dữ liệu và Trí tuệ nhân tạo",        "chi_tieu": 70,  "diem_chuan_2025": 26.13},
    {"so": 39, "ten_chuong_trinh": "Trí tuệ nhân tạo",                   "ma_xet_tuyen": "EP16",      "ma_nganh": "7480107", "ten_nganh": "Trí tuệ nhân tạo",                       "khoa_vien": "Khoa Khoa học dữ liệu và Trí tuệ nhân tạo",        "chi_tieu": 80,  "diem_chuan_2025": 25.44},
    {"so": 40, "ten_chuong_trinh": "Kỹ thuật phần mềm",                  "ma_xet_tuyen": "EP17",      "ma_nganh": "7480103", "ten_nganh": "Kỹ thuật phần mềm",                      "khoa_vien": "Khoa Công nghệ thông tin",                         "chi_tieu": 50,  "diem_chuan_2025": 24.68},
    {"so": 41, "ten_chuong_trinh": "Quản trị giải trí và sự kiện",       "ma_xet_tuyen": "EP18",      "ma_nganh": "7810101", "ten_nganh": "Du lịch",                                "khoa_vien": "Khoa Du lịch và Khách sạn",                       "chi_tieu": 50,  "diem_chuan_2025": 25.89},
    {"so": 42, "ten_chuong_trinh": "Quản lý công và Chính sách (E-PMP)", "ma_xet_tuyen": "EPMP",      "ma_nganh": "7340403", "ten_nganh": "Quản lý công",                           "khoa_vien": "Khoa Khoa học quản lý",                           "chi_tieu": 70,  "diem_chuan_2025": 23.04},
    # ── Hệ Đại trà / Chính quy ────────────────────────────────────────────
    {"so": 57, "ten_chuong_trinh": "Kinh tế học",                         "ma_xet_tuyen": "7310101_1", "ma_nganh": "7310101", "ten_nganh": "Kinh tế",                                "khoa_vien": "Khoa Kinh tế học",                                 "chi_tieu": 50,  "diem_chuan_2025": 26.52},
    {"so": 62, "ten_chuong_trinh": "Kinh tế và quản lý đô thị",           "ma_xet_tuyen": "7310101_2", "ma_nganh": "7310101", "ten_nganh": "Kinh tế",                                "khoa_vien": "Khoa Môi trường, Biến đổi khí hậu và Đô thị",      "chi_tieu": 50,  "diem_chuan_2025": 25.86},
    {"so": 63, "ten_chuong_trinh": "Kinh tế và quản lý nguồn nhân lực",   "ma_xet_tuyen": "7310101_3", "ma_nganh": "7310101", "ten_nganh": "Kinh tế",                                "khoa_vien": "Khoa Kinh tế và Quản lý nguồn nhân lực",           "chi_tieu": 50,  "diem_chuan_2025": 26.79},
    # ── TT1 / TT2 ─────────────────────────────────────────────────────────
    {"so": 84, "ten_chuong_trinh": "Kế toán (TT1)",                       "ma_xet_tuyen": "TT1",       "ma_nganh": "7340301", "ten_nganh": "Kế toán",                                "khoa_vien": "Viện Kế toán - Kiểm toán",                         "chi_tieu": 55,  "diem_chuan_2025": 24.75},
    {"so": 85, "ten_chuong_trinh": "Kế hoạch tài chính (TT1)",            "ma_xet_tuyen": "TT1",       "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                       "chi_tieu": 55,  "diem_chuan_2025": 24.75},
    {"so": 86, "ten_chuong_trinh": "Quản trị kinh doanh (TT1)",           "ma_xet_tuyen": "TT1",       "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                    "khoa_vien": "Khoa Quản trị kinh doanh",                         "chi_tieu": 55,  "diem_chuan_2025": 24.75},
    {"so": 87, "ten_chuong_trinh": "Tài chính (TT2)",                     "ma_xet_tuyen": "TT2",       "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                       "chi_tieu": 220, "diem_chuan_2025": 25.5},
    {"so": 88, "ten_chuong_trinh": "Kinh doanh quốc tế (TT2)",            "ma_xet_tuyen": "TT2",       "ma_nganh": "7340120", "ten_nganh": "Kinh doanh quốc tế",                     "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",               "chi_tieu": 110, "diem_chuan_2025": 25.5},
    # ── CLC ───────────────────────────────────────────────────────────────
    {"so": 89, "ten_chuong_trinh": "Kinh tế phát triển (CLC1)",            "ma_xet_tuyen": "CLC1",      "ma_nganh": "7310105", "ten_nganh": "Kinh tế phát triển",                     "khoa_vien": "Khoa Kế hoạch và Phát triển",                      "chi_tieu": 55,  "diem_chuan_2025": 25.25},
    {"so": 90, "ten_chuong_trinh": "Ngân hàng (CLC1)",                    "ma_xet_tuyen": "CLC1",       "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                       "chi_tieu": 55,  "diem_chuan_2025": 25.25},
    {"so": 91, "ten_chuong_trinh": "Công nghệ thông tin và chuyển đổi số (CLC1)", "ma_xet_tuyen": "CLC1", "ma_nganh": "7480201", "ten_nganh": "Công nghệ thông tin",               "khoa_vien": "Khoa Công nghệ thông tin",                          "chi_tieu": 55,  "diem_chuan_2025": 25.25},
    {"so": 92, "ten_chuong_trinh": "Bảo hiểm tích hợp chứng chỉ ANZIIF (CLC1)", "ma_xet_tuyen": "CLC1", "ma_nganh": "7340204", "ten_nganh": "Bảo hiểm",                           "khoa_vien": "Khoa Bảo hiểm",                                    "chi_tieu": 55,  "diem_chuan_2025": 25.25},
    {"so": 93, "ten_chuong_trinh": "Kinh tế đầu tư (CLC2)",               "ma_xet_tuyen": "CLC2",      "ma_nganh": "7310104", "ten_nganh": "Kinh tế đầu tư",                         "khoa_vien": "Khoa Đầu tư",                                      "chi_tieu": 160, "diem_chuan_2025": 26.5},
    {"so": 94, "ten_chuong_trinh": "Quản trị nhân lực (CLC2)",             "ma_xet_tuyen": "CLC2",      "ma_nganh": "7340404", "ten_nganh": "Quản trị nhân lực",                      "khoa_vien": "Khoa Kinh tế và Quản lý nguồn nhân lực",           "chi_tieu": 160, "diem_chuan_2025": 26.5},
    {"so": 95, "ten_chuong_trinh": "Quản trị kinh doanh (CLC2)",           "ma_xet_tuyen": "CLC2",      "ma_nganh": "7340101", "ten_nganh": "Quản trị kinh doanh",                    "khoa_vien": "Khoa Quản trị kinh doanh",                         "chi_tieu": 105, "diem_chuan_2025": 26.5},
    {"so": 96, "ten_chuong_trinh": "Quan hệ công chúng (CLC2)",            "ma_xet_tuyen": "CLC2",      "ma_nganh": "7320108", "ten_nganh": "Quan hệ công chúng",                     "khoa_vien": "Khoa Marketing",                                   "chi_tieu": 160, "diem_chuan_2025": 26.5},
    {"so": 97, "ten_chuong_trinh": "Tài chính doanh nghiệp (CLC3)",        "ma_xet_tuyen": "CLC3",      "ma_nganh": "7340201", "ten_nganh": "Tài chính Ngân hàng",                    "khoa_vien": "Viện Ngân hàng - Tài chính",                       "chi_tieu": 325, "diem_chuan_2025": 26.42},
    {"so": 98, "ten_chuong_trinh": "Marketing số (CLC3)",                  "ma_xet_tuyen": "CLC3",      "ma_nganh": "7340115", "ten_nganh": "Marketing",                              "khoa_vien": "Khoa Marketing",                                   "chi_tieu": 270, "diem_chuan_2025": 26.42},
    {"so": 99, "ten_chuong_trinh": "Quản trị Marketing (CLC3)",            "ma_xet_tuyen": "CLC3",      "ma_nganh": "7340115", "ten_nganh": "Marketing",                              "khoa_vien": "Khoa Marketing",                                   "chi_tieu": 165, "diem_chuan_2025": 26.42},
    {"so": 100,"ten_chuong_trinh": "Quản trị kinh doanh quốc tế (CLC3)",  "ma_xet_tuyen": "CLC3",      "ma_nganh": "7340120", "ten_nganh": "Kinh doanh quốc tế",                     "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",               "chi_tieu": 270, "diem_chuan_2025": 26.42},
    {"so": 101,"ten_chuong_trinh": "Kinh tế quốc tế (CLC3)",               "ma_xet_tuyen": "CLC3",      "ma_nganh": "7310106", "ten_nganh": "Kinh tế quốc tế",                        "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",               "chi_tieu": 270, "diem_chuan_2025": 26.42},
    {"so": 102,"ten_chuong_trinh": "Logistics và quản lý chuỗi cung ứng (CLC3)", "ma_xet_tuyen": "CLC3", "ma_nganh": "7510605", "ten_nganh": "Logistics và Quản lý chuỗi cung ứng",  "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",               "chi_tieu": 165, "diem_chuan_2025": 26.42},
    {"so": 103,"ten_chuong_trinh": "Thương mại điện tử (CLC3)",             "ma_xet_tuyen": "CLC3",      "ma_nganh": "7340122", "ten_nganh": "Thương mại điện tử",                     "khoa_vien": "Viện Thương mại và Kinh tế quốc tế",               "chi_tieu": 165, "diem_chuan_2025": 26.42},
    {"so": 104,"ten_chuong_trinh": "Kiểm toán tích hợp chứng chỉ ACCA (CLC3)", "ma_xet_tuyen": "CLC3", "ma_nganh": "7340302", "ten_nganh": "Kiểm toán",                             "khoa_vien": "Viện Kế toán - Kiểm toán",                         "chi_tieu": 270, "diem_chuan_2025": 26.42},
]


_ADMISSION_PATTERN = re.compile(
    r"chỉ\s*tiêu"
    r"|điểm\s*chuẩn"
    r"|điểm\s*đầu\s*vào"
    r"|tuyển\s*sinh"
    r"|xét\s*tuyển"
    r"|mã\s*xét\s*tuyển"
    r"|POHE|CLC[123]|TT[12]|E-BBA|EP\d+",
    _F,
)


_MAJOR_SYNONYMS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"kinh\s*doanh\s*nông\s*nghiệp", _F), "kinh tế nông nghiệp"),
    (re.compile(r"quản\s*trị\s*nông\s*nghiệp", _F), "kinh tế nông nghiệp"),
    (re.compile(r"tài\s*chính\s*doanh\s*nghiệp", _F), "tài chính ngân hàng"),
    (re.compile(r"ngân\s*hàng\s*số", _F), "công nghệ tài chính và ngân hàng số"),
    (re.compile(r"cntt|công\s*nghệ\s*tt", _F), "công nghệ thông tin"),
    (re.compile(r"khoa\s*học\s*máy\s*tính", _F), "công nghệ thông tin"),
    (re.compile(r"kỹ\s*thuật\s*điện\s*tử", _F), "kỹ thuật phần mềm"),
    (re.compile(r"marketing\s*số|digital\s*marketing", _F), "marketing số"),
    (re.compile(r"pr\b|quan\s*hệ\s*công\s*chúng", _F), "quan hệ công chúng"),
    (re.compile(r"logistics\b(?!.*chuỗi)", _F), "logistics và quản lý chuỗi cung ứng"),
    (re.compile(r"thương\s*mại\s*điện\s*tử|tmđt|e-commerce", _F), "thương mại điện tử"),
    (re.compile(r"kinh\s*tế\s*số(?!.*dự\s*kiến)", _F), "kinh tế số"),
    (re.compile(r"trí\s*tuệ\s*nhân\s*tạo|ai\b|artificial\s*intelligence", _F), "trí tuệ nhân tạo"),
    (re.compile(r"khoa\s*học\s*dữ\s*liệu|data\s*science", _F), "khoa học dữ liệu"),
]

_MAJOR_SYNONYMS.extend(_MAJOR_SYNONYMS_TAXONOMY_ADDITIONS)


def _apply_major_synonyms(question: str) -> str:
    q = question
    for pattern, canonical in _MAJOR_SYNONYMS:
        q = pattern.sub(canonical, q)
    return q


def search_admission_data(question: str) -> list[dict]:
    question = _apply_major_synonyms(question)
    q_lower = question.lower()

    # 1. Match explicit program codes
    ma_xt_pattern = re.compile(r"\b(EP\d+|POHE\d*|EBBA|EPMP|CLC[123]|TT[12])\b", re.IGNORECASE)
    found_codes = [m.group(1).upper() for m in ma_xt_pattern.finditer(question)]
    if found_codes:
        results = [e for e in ADMISSION_DATA if e["ma_xet_tuyen"].upper() in found_codes]
        if results:
            return results

    # 2. Match 7-digit major codes
    results = [e for e in ADMISSION_DATA if re.search(r"\b" + re.escape(e["ma_nganh"]) + r"\b", question)]
    if results:
        return results

    # 3. Extract term by removing context words, then substring match
    context_pat = re.compile(
        r"điểm\s*chuẩn|điểm\s*đầu\s*vào|chỉ\s*tiêu|tuyển\s*sinh"
        r"|chương\s*trình\s*đào\s*tạo|chương\s*trình|đào\s*tạo"
        r"|ngành\s*học|ngành|ctđt|năm\s*\d{4}|\b20\d{2}\b"
        r"|bao\s*nhiêu|của\s*trường|tại\s*neu|tại\s*trường"
        r"|\blà\s*bao\s*nhiêu\b|\blà\s*gì\b|\blà\b"
        r"|\bnhư\s*thế\s*nào\b|\bthế\s*nào\b|\bcủa\b|\bcó\b"
        r"|\bcho\s*tôi\s*biết\b|\bcho\s*biết\b|\bxin\s*hỏi\b|\bhỏi\b",
        _F,
    )
    term = context_pat.sub(" ", q_lower)
    term = re.sub(r"\s+", " ", term).strip()
    if not term:
        return []

    def normalize(s: str) -> str:
        s = re.sub(r"[\(\)\[\]\-_/\\,\.]+", " ", s)
        return re.sub(r"\s+", " ", s).strip()

    term_norm = normalize(term)
    exact_matches = []
    for entry in ADMISSION_DATA:
        name_norm = normalize(entry["ten_chuong_trinh"].lower())
        nganh_norm = normalize(entry["ten_nganh"].lower())
        if term_norm in name_norm or term_norm in nganh_norm:
            exact_matches.append(entry)

    if exact_matches:
        name_hits = [e for e in exact_matches if term_norm in normalize(e["ten_chuong_trinh"].lower())]
        if name_hits:
            exact_name_hits = [e for e in name_hits if term_norm == normalize(e["ten_chuong_trinh"].lower())]
            return exact_name_hits or name_hits
        term_words = set(term.split())
        nganh_hits = [
            e for e in exact_matches
            if any(w in normalize(e["ten_chuong_trinh"].lower()) for w in term_words)
        ]
        return nganh_hits if nganh_hits else exact_matches

    # 4. Fallback scoring
    words = [w for w in term.split() if len(w) >= 2]
    if not words:
        return []

    scored = []
    for entry in ADMISSION_DATA:
        name_lower = entry["ten_chuong_trinh"].lower()
        nganh_lower = entry["ten_nganh"].lower()
        name_score = 0
        nganh_score = 0

        for length in range(min(len(words), 6), 1, -1):
            for i in range(len(words) - length + 1):
                phrase = " ".join(words[i:i + length])
                if phrase in name_lower:
                    name_score += length * 5
                if phrase in nganh_lower:
                    nganh_score += length * 2

        for w in words:
            if w in name_lower:
                name_score += 1
            if w in nganh_lower:
                nganh_score += 1

        total = name_score + nganh_score
        if total > 0:
            scored.append((name_score, total, entry))

    if not scored:
        return []

    has_name_match = any(ns > 0 for ns, _, _ in scored)
    if has_name_match:
        scored = [(ns, tot, e) for ns, tot, e in scored if ns > 0]
        max_score = max(ns for ns, _, _ in scored)
        filtered = [e for ns, _, e in scored if ns >= max_score * 0.75]
    else:
        max_score = max(tot for _, tot, _ in scored)
        filtered = [e for _, tot, e in scored if tot >= max_score * 0.75]

    seen = set()
    unique = []
    for e in filtered:
        key = e["ma_xet_tuyen"] + e["ma_nganh"]
        if key not in seen:
            seen.add(key)
            unique.append(e)
    return unique


def format_admission_answer(question: str, programs: list[dict]) -> str:
    if not programs:
        return "Hiện chưa tìm thấy chương trình phù hợp với câu hỏi của bạn."

    q_lower = question.lower()
    want_diem = bool(re.search(r"điểm.{0,5}chuẩn|điểm.{0,5}đầu vào", q_lower))
    want_chitieu = bool(re.search(r"chỉ.{0,3}tiêu", q_lower))

    def one_line(p: dict) -> str:
        ten = p["ten_chuong_trinh"]
        ma = p["ma_nganh"]
        ct = p["chi_tieu"]
        dc = p["diem_chuan_2025"]
        diem_str = str(dc) if dc is not None else None
        if want_diem and not want_chitieu:
            if diem_str is None:
                return f"- **{ten}** (mã {ma}): chương trình này chưa cập nhật điểm chuẩn"
            return f"- **{ten}** (mã {ma}): điểm chuẩn 2025 là **{diem_str}**"
        if want_chitieu and not want_diem:
            return f"- **{ten}** (mã {ma}): chỉ tiêu **{ct} sinh viên**"
        diem_part = f"**{diem_str}**" if diem_str is not None else "chưa cập nhật"
        return f"- **{ten}** (mã {ma}): chỉ tiêu **{ct} sinh viên**, điểm chuẩn 2025: {diem_part}"

    if len(programs) == 1:
        p = programs[0]
        ten = p["ten_chuong_trinh"]
        ma = p["ma_nganh"]
        ct = p["chi_tieu"]
        dc = p["diem_chuan_2025"]
        diem_str = str(dc) if dc is not None else None
        if want_diem and not want_chitieu:
            if diem_str is None:
                return f"Chương trình **{ten}** (mã ngành {ma}) chưa cập nhật điểm chuẩn."
            return f"Chương trình **{ten}** (mã ngành {ma}) có điểm chuẩn 2025 là **{diem_str}**."
        if want_chitieu and not want_diem:
            return f"Chương trình **{ten}** (mã ngành {ma}) có chỉ tiêu tuyển sinh 2026 là **{ct} sinh viên**."
        diem_part = f"**{diem_str}**" if diem_str is not None else "chưa cập nhật"
        return (
            f"Chương trình **{ten}** (mã ngành {ma}): "
            f"chỉ tiêu **{ct} sinh viên**, điểm chuẩn 2025: {diem_part}."
        )

    lines = ["Dưới đây là thông tin tuyển sinh các chương trình phù hợp:"]
    for p in programs:
        lines.append(one_line(p))
    return "\n".join(lines)


def _extract_admission_term(question: str) -> tuple[str, str]:
    code_match = re.search(r"\b(7\d{6})\b", question)
    code = code_match.group(1) if code_match else ""
    context_pat = re.compile(
        r"điểm\s*chuẩn|điểm\s*đầu\s*vào|chỉ\s*tiêu|tuyển\s*sinh"
        r"|chương\s*trình\s*đào\s*tạo|chương\s*trình|đào\s*tạo"
        r"|ngành\s*học|ngành|ctđt|năm\s*\d{4}|\b20\d{2}\b"
        r"|bao\s*nhiêu|của\s*trường|tại\s*neu|tại\s*trường"
        r"|\blà\s*bao\s*nhiêu\b|\blà\s*gì\b|\blà\b"
        r"|\bnhư\s*thế\s*nào\b|\bthế\s*nào\b|\bcủa\b|\bcó\b"
        r"|\bcho\s*tôi\s*biết\b|\bcho\s*biết\b|\bxin\s*hỏi\b|\bhỏi\b",
        _F,
    )
    term = context_pat.sub(" ", question.lower())
    term = re.sub(r"\s+", " ", term).strip()
    return term, code


def query_neo4j_major_admission(driver, question: str) -> list[dict]:
    term, code = _extract_admission_term(question)
    special_code_pat = re.compile(r"\b(EP\d+|POHE\d*|EBBA|EPMP|CLC[123]|TT[12])\b", re.IGNORECASE)
    if special_code_pat.search(question):
        return []

    cypher = """
        MATCH (m:MAJOR)
        WHERE (
            ($code <> '' AND m.code STARTS WITH $code)
            OR ($term <> '' AND (
                toLower(m.name)    CONTAINS toLower($term)
                OR toLower(m.name_vi) CONTAINS toLower($term)
            ))
        )
        AND (m.diem_chuan IS NOT NULL OR m.chi_tieu IS NOT NULL)
        RETURN m.name      AS name,
               m.name_vi   AS name_vi,
               m.code      AS code,
               m.diem_chuan AS diem_chuan,
               m.chi_tieu   AS chi_tieu,
               m.khoa_vien  AS khoa_vien
        ORDER BY m.code
        LIMIT 10
    """
    try:
        with driver.session() as session:
            rows = session.run(cypher, term=term, code=code).data()
    except Exception:
        return []

    results = []
    for r in rows:
        name = r.get("name_vi") or r.get("name") or ""
        results.append(
            {
                "ten_chuong_trinh": name,
                "ma_nganh": r.get("code", ""),
                "chi_tieu": r.get("chi_tieu"),
                "diem_chuan_2025": r.get("diem_chuan"),
                "khoa_vien": r.get("khoa_vien", ""),
                "_source": "neo4j",
            }
        )
    return results


def handle_admission_question(question: str, driver=None) -> str | None:
    if not _ADMISSION_PATTERN.search(question):
        return None

    q_lower = question.lower()
    is_general = bool(
        re.search(
            r"t[aấ]t\s*c[aả]|to[àa]n\s*b[ộo]|c[aá]c\s*ng[àa]nh|danh\s*s[aá]ch|li[eê]t\s*k[eê]",
            q_lower,
        )
    )
    if is_general:
        return (
            "NEU có hơn 100 chương trình đào tạo. "
            "Bạn có thể hỏi cụ thể từng ngành để tôi tra chỉ tiêu và điểm chuẩn, "
            "hoặc xem toàn bộ danh sách tại tuyensinh.neu.edu.vn."
        )

    if driver is not None:
        neo4j_programs = query_neo4j_major_admission(driver, question)
        if neo4j_programs:
            return format_admission_answer(question, neo4j_programs)

    programs = search_admission_data(question)
    if not programs:
        return "Hiện chưa tìm thấy thông tin tuyển sinh cho ngành bạn hỏi. Bạn có thể xem thêm tại tuyensinh.neu.edu.vn."
    return format_admission_answer(question, programs)


__all__ = [
    "ADMISSION_DATA",
    "handle_admission_question",
    "query_neo4j_major_admission",
    "search_admission_data",
]

