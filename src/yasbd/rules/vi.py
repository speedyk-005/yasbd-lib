from yasbd.rules.base import Rules


# fmt: off
class ViRules(Rules):


    TITLE_ABBRVS = Rules.TITLE_ABBRVS | {
        # Core Academic and Medical Acronyms
        "GS", "PGS", "TS", "ThS", "BS",

        # Compound Professional Titles
        "ThS.BS", "PGS.TS", "GS.TS", "TH.S",

        # Technical and Political Honorifics
        "KTS", "đ/c", "Đ/c"
    }

    DOTTED_GEOPOL_ABBRVS = Rules.DOTTED_GEOPOL_ABBRVS | {
        "V.N", "T.G", "T.Ư",
    }

    REFERENCE_ABBRVS = Rules.REFERENCE_ABBRVS | {
        "tr", "ch", "q", "t", "m", "stt", "hđ", "nxb"
    }

    SECTION_MARKERS = Rules.SECTION_MARKERS | {
        "Phần", "Chương", "Mục", "Điều", "Khoản", "Điểm",
        "Phụ lục", "Lời mở đầu"
    }

    INLINE_ONLY_ABBRVS = Rules.INLINE_ONLY_ABBRVS | {
        "v.v", "t.l", "t.m", "p.v"
    }

    COMMON_SENT_STARTERS = Rules.COMMON_SENT_STARTERS | {
        # Articles
        "Cái", "Chiếc", "Con", "Sự", "Việc", "Niềm", "Cuộc", "Các", "Những",

        # Pronouns & Demonstratives
        "Tôi", "Bạn", "Nó", "Anh", "Chị", "Ông", "Bà", "Chúng tôi", "Họ",
        "Đây", "Đó", "Kia", "Này",

        # Adverbs & Logical Connectors
        "Nhưng", "Vì vậy", "Do đó", "Tuy nhiên", "Mặc dù",
        "Vậy", "Sau đó", "Tiếp theo", "Hiện tại", "Cuối cùng",
        "Ban đầu", "Sau khi", "Tiếp tục", "Cuối", "Đầu tiên",
        "Thứ hai", "Thứ ba", "Trước đây", "Từ nay",
        "Cho đến nay",

        # Question words
        "Ai", "Cái gì", "Gì", "Khi nào", "Đâu", "Tại sao", "Như thế nào", "Bao nhiêu",
        "Nào",

        # Other common starters
        "Có phải", "Triệu",
    }

# fmt: on
