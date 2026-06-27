import re
from itertools import chain

from yasbd.rules.base import Rules, _build_abbr_pattern


# fmt: off
class ThRules(Rules):


    # Thai periods are commonly used in abbreviations rather than
    # as sentence terminators. Traditional end-of-text marks ๚ and ๛
    # may appear in literary or formal contexts.
    TERMINATORS = (Rules.TERMINATORS - {"."}) | {"๚", "๛"}

    TITLE_ABBRVS = set()
    DOTTED_GEOPOL_ABBRVS = set()
    REFERENCE_ABBRVS = set()
    SECTION_MARKERS = set()
    DATE_ABBRVS = set()

    COMMON_SENT_STARTERS = {
        # Discourse resets (temporal, sequencing, causal, contrast)
        "เมื่อสมัย", "ต่อมา", "ภายหลัง", "สุดท้าย",
        "จากนั้น", "ต่อจากนั้น",
        "ดังนั้น", "เพราะฉะนั้น",
        "อย่างไรก็ตาม", "ทว่า", "ถึงอย่างนั้น",

        # Discourse framing & explanation
        "สรุป", "สรุปว่า", "กล่าวโดยสรุป", "สุดท้ายนี้",
        "กล่าวคือ", "ตัวอย่างเช่น",

        # Question words
        "อะไร", "ใคร", "ที่ไหน", "เมื่อไร", "เมื่อไหร่",
        "ทำไม", "อย่างไร", "เท่าไร", "เท่าไหร่", "กี่",

        # Pronouns
        "ผม", "เขา", "เธอ", "เรา", "คุณ", "มัน",
        "ดิฉัน", "เค้า", "พวกเรา", "พวกเขา",

        # Post-discourse-particle clause starts
        "กำลัง",
    }

    REPORTING_VERBS = {
        "บอก", "พูด", "กล่าว", "ถาม", "ตอบ","อธิบาย",
         "รายงาน", "เสนอ", "ยืนยัน", "เขียน"
    }

    DISCOURSE_FINAL_PARTICLES = {
        # polite closure markers
        "ครับ", "นะครับ", "ค่ะ", "คะ", "นะคะ", "ครับผม", "เจ้าค่ะ",
        "จ้า", "จ๊ะ", "จ้ะ", "ฮะ",

        # interrogative / clause-final question markers
        "ไหม", "มั้ย", "หรือยัง", "หรือไม่", "รึเปล่า",
        "เหรอ", "ป่าว", "ล่ะ",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        """Override base regex compilation"""
        super()._compile_regex_dynamically()

        cls.FINAL_PARTICLES_FINDER = re.compile(
            rf"{_build_abbr_pattern(cls.DISCOURSE_FINAL_PARTICLES)}(?![\s]*[.?!;:๚๛])"
        )

        cls.SPACE_PLUS_STARTER_FINDER = re.compile(
            rf"(?!\.\s*)(?=\s{cls.COMMON_STARTERS_PATTERN})"
        )

    def _post_process_boundaries(
        self, main_boundaries: set[int], text: str
    ) -> None:
        main_boundaries.update(
            m.end() for m in
            chain(
                self.FINAL_PARTICLES_FINDER.finditer(text),
                self.SPACE_PLUS_STARTER_FINDER.finditer(text),
            )
        )
