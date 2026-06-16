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
        "เมื่อ", "เมื่อสมัย", "เมื่อก่อน", "เมื่อครั้ง",
        "หลังจาก", "ต่อมา", "ภายหลัง", "ทันที", "สุดท้าย",
        "จากนั้น", "ต่อจากนั้น", "แล้ว", "แล้วก็", "แล้วจึง",
        "ดังนั้น", "เพราะฉะนั้น",
        "อย่างไรก็ตาม", "แต่", "ทว่า", "ถึงอย่างนั้น",

        # Discourse framing & explanation
        "สรุป", "สรุปว่า", "กล่าวโดยสรุป", "สุดท้ายนี้",
        "กล่าวคือ", "ตัวอย่างเช่น", "เพราะ",

        # Post-discourse-particle clause starts
        "ผม", "เจอ", "กำลัง",
    }

    REPORTING_VERBS = {
        "บอก", "พูด", "กล่าว", "ถาม", "ตอบ","อธิบาย",
         "รายงาน", "เสนอ", "ยืนยัน", "เขียน"
    }

    DISCOURSE_FINAL_PARTICLES = {
        # polite closure markers
        "ครับ", "ค่ะ", "คะ", "ครับผม", "เจ้าค่ะ",
        "จ้า", "จ๊ะ", "จ้ะ",

        # interrogative / clause-final question markers
        "ไหม", "มั้ย", "หรือยัง", "รึเปล่า", "เหรอ",
        "ป่าว", "ล่ะ",
    }

    # fmt: on
    @classmethod
    def _compile_regex_dynamically(cls):
        super()._compile_regex_dynamically()

        cls.FINAL_PARTICLES_FINDER = re.compile(rf"""
            {_build_abbr_pattern(cls.DISCOURSE_FINAL_PARTICLES)}
            (?={cls.COMMON_STARTERS_PATTERN})
            """, re.X
        )

        cls.SPACE_PLUS_STARTER_FINDER = re.compile(
            rf"(?=\s{cls.COMMON_STARTERS_PATTERN})"
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
