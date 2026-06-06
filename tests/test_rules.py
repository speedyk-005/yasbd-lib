"""Tests for new and modified rule classes introduced in this PR.

Covers:
  - ArRules (new)
  - PtRules (new)
  - RuRules (new)
  - ZhRules (new)
  - JaRules (modified: removed CASE_MARKERS / GEOPOLITICAL_ABBRVS, new fullwidth regex)
  - Rules base class (modified: new reference abbrvs, removed CONTIGUOUS_TERMINATORS_FINDER,
    new superscript indicator, changed NAIVE_BOUNDARY_FINDER cluster handling)
"""

import pytest

from yasbd import BoundaryDetector
from yasbd.rules.ar import ArRules
from yasbd.rules.base import Rules
from yasbd.rules.ja import JaRules
from yasbd.rules.pt import PtRules
from yasbd.rules.ru import RuRules
from yasbd.rules.zh import ZhRules


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def ar_rules():
    return ArRules()


@pytest.fixture(scope="module")
def pt_rules():
    return PtRules()


@pytest.fixture(scope="module")
def ru_rules():
    return RuRules()


@pytest.fixture(scope="module")
def zh_rules():
    return ZhRules()


@pytest.fixture(scope="module")
def ja_rules():
    return JaRules()


@pytest.fixture(scope="module")
def base_rules():
    return Rules()


@pytest.fixture(scope="module")
def ar_detector():
    return BoundaryDetector(lang="ar")


@pytest.fixture(scope="module")
def pt_detector():
    return BoundaryDetector(lang="pt")


@pytest.fixture(scope="module")
def ru_detector():
    return BoundaryDetector(lang="ru")


@pytest.fixture(scope="module")
def zh_detector():
    return BoundaryDetector(lang="zh")


# ---------------------------------------------------------------------------
# base.py — attribute changes
# ---------------------------------------------------------------------------


class TestBaseRulesChanges:
    """Tests for attributes and patterns that were modified in base.py."""

    def test_reference_abbrvs_contains_diag(self, base_rules):
        """'diag' was added to REFERENCE_ABBRVS in this PR."""
        assert "diag" in Rules.REFERENCE_ABBRVS

    def test_reference_abbrvs_contains_n_ordinal(self, base_rules):
        """'n.º' (ordinal number abbreviation) was added to REFERENCE_ABBRVS in this PR."""
        assert "n.º" in Rules.REFERENCE_ABBRVS

    def test_contiguous_terminators_finder_removed(self, base_rules):
        """CONTIGUOUS_TERMINATORS_FINDER was removed from the Rules class in this PR."""
        assert not hasattr(base_rules, "CONTIGUOUS_TERMINATORS_FINDER")

    def test_fullwidth_geopolitical_abbrvs_not_exported(self):
        """FULLWIDTH_GEOPOLITICAL_ABBRVS was removed from base module in this PR."""
        import yasbd.rules.base as base_module

        assert not hasattr(base_module, "FULLWIDTH_GEOPOLITICAL_ABBRVS")

    def test_mid_sentence_finder_has_superscript_pattern(self, base_rules):
        """A new dot-before-superscript pattern (\.(?=[ºª])) was added."""
        patterns = [p.pattern for p in Rules.MID_SENTENCE_FINDER_LST]
        assert any(r"(?=[ºª])" in pat for pat in patterns), (
            "Expected a superscript-indicator pattern in MID_SENTENCE_FINDER_LST"
        )

    def test_superscript_indicator_no_split_before_ordinal(self):
        """n.º and 1.º should not create a sentence boundary."""
        rules = Rules()
        # "n.º 15" mid-sentence — should produce only one sentence
        text = "O artigo n.º 15 está em vigor."
        boundaries = rules.apply(text, preserve_quote_and_paren=True)
        # Only the start (0) and end (len) should be boundaries
        assert boundaries == [0, len(text)], (
            f"Unexpected boundaries for superscript ordinal: {boundaries}"
        )

    def test_naive_boundary_finder_no_split_inside_terminator_cluster(self):
        """Terminator clusters like !!! should not produce interior splits."""
        rules = Rules()
        text = "Hello!!!"
        boundaries = rules.apply(text, preserve_quote_and_paren=True)
        # Only the start and end — no interior boundary inside !!!
        assert boundaries == [0, len(text)], (
            f"Interior split inside terminator cluster: {boundaries}"
        )

    def test_naive_boundary_finder_splits_after_terminator_cluster(self):
        """After a cluster like !!, a new sentence should start."""
        rules = Rules()
        text = "Hello!! New sentence."
        boundaries = rules.apply(text, preserve_quote_and_paren=True)
        # Should split somewhere between the two sentences
        assert len(boundaries) > 2, (
            f"Expected a split after terminator cluster; boundaries: {boundaries}"
        )


# ---------------------------------------------------------------------------
# ArRules — new Arabic rules
# ---------------------------------------------------------------------------


class TestArRulesAttributes:
    def test_terminators_includes_arabic_question_mark(self):
        """ArRules must include the Arabic question mark ؟."""
        assert "؟" in ArRules.TERMINATORS

    def test_terminators_inherits_base(self):
        """ArRules TERMINATORS should be a superset of base TERMINATORS."""
        assert Rules.TERMINATORS.issubset(ArRules.TERMINATORS)

    def test_case_markers_arabic(self):
        """ArRules.CASE_MARKERS should contain Arabic clitic prepositions."""
        assert "بـ" in ArRules.CASE_MARKERS
        assert "لـ" in ArRules.CASE_MARKERS
        assert "كـ" in ArRules.CASE_MARKERS
        assert "فـ" in ArRules.CASE_MARKERS
        assert "وـ" in ArRules.CASE_MARKERS

    def test_reporting_words_arabic(self):
        """ArRules.REPORTING_WORDS should contain common Arabic speech verbs."""
        assert "قال" in ArRules.REPORTING_WORDS
        assert "تقول" in ArRules.REPORTING_WORDS
        assert "أضاف" in ArRules.REPORTING_WORDS
        assert "أكد" in ArRules.REPORTING_WORDS
        assert "أوضح" in ArRules.REPORTING_WORDS

    def test_heading_tokens_arabic(self):
        """ArRules.HEADING_TOKENS should contain Arabic structural headings."""
        assert "فصل" in ArRules.HEADING_TOKENS
        assert "باب" in ArRules.HEADING_TOKENS
        assert "قسم" in ArRules.HEADING_TOKENS
        assert "الفصل" in ArRules.HEADING_TOKENS

    def test_reference_abbrvs_arabic(self):
        """ArRules.REFERENCE_ABBRVS should contain Arabic reference markers."""
        assert "ص" in ArRules.REFERENCE_ABBRVS
        assert "ج" in ArRules.REFERENCE_ABBRVS
        assert "انظر" in ArRules.REFERENCE_ABBRVS

    def test_common_sent_starters_arabic(self):
        """ArRules.COMMON_SENT_STARTERS should contain Arabic transition words."""
        assert "ولكن" in ArRules.COMMON_SENT_STARTERS
        assert "لذلك" in ArRules.COMMON_SENT_STARTERS
        assert "غير" in ArRules.COMMON_SENT_STARTERS

    def test_geopolitical_abbrvs_extends_base(self):
        """ArRules.GEOPOLITICAL_ABBRVS should be a superset of base."""
        assert "U.S" in ArRules.GEOPOLITICAL_ABBRVS
        assert "و.م.أ" in ArRules.GEOPOLITICAL_ABBRVS

    def test_mid_sentence_abbrvs_extends_base(self):
        """ArRules.MID_SENTENCE_ABBRVS should include Arabic time/era abbreviations."""
        assert "هـ" in ArRules.MID_SENTENCE_ABBRVS
        assert "إلخ" in ArRules.MID_SENTENCE_ABBRVS
        assert "ص.ب" in ArRules.MID_SENTENCE_ABBRVS

    def test_ellipsis_pattern_added_to_mid_sentence_finders(self, ar_rules):
        """_compile_regex_dynamically should append an ellipsis-protection pattern."""
        patterns = [p.pattern for p in ArRules.MID_SENTENCE_FINDER_LST]
        assert any(r"\.{3,}" in pat for pat in patterns), (
            "Expected an ellipsis pattern in ArRules.MID_SENTENCE_FINDER_LST"
        )


class TestArRulesSegmentation:
    def test_arabic_question_mark_splits(self, ar_detector):
        """؟ should trigger a sentence boundary in Arabic text."""
        result = list(ar_detector.segment("ما اسمك؟ اسمي أحمد."))
        assert len(result) == 2
        assert result[0] == "ما اسمك؟"
        assert result[1] == "اسمي أحمد."

    def test_arabic_basic_period_splits(self, ar_detector):
        """Standard period should split Arabic sentences."""
        result = list(ar_detector.segment("مرحباً بالعالم. كيف حالك؟"))
        assert len(result) == 2

    def test_arabic_ellipsis_no_split(self, ar_detector):
        """Ellipsis (...) should not create a sentence boundary in Arabic."""
        result = list(ar_detector.segment("فكر... لكنه لم يقل شيئاً."))
        assert len(result) == 1, (
            f"Ellipsis should not split: got {result}"
        )

    def test_arabic_heading_no_split(self, ar_detector):
        """Structural headings like 'فصل ١.' should not split mid-heading."""
        text = "فصل ١. البداية. كان المكان مظلمًا."
        result = list(ar_detector.segment(text))
        # Should split at "البداية." not inside "فصل ١."
        assert result[0] == "فصل ١. البداية."

    def test_arabic_title_abbrvs_no_split(self, ar_detector):
        """Title abbreviations like 'د.' should not split mid-sentence."""
        result = list(ar_detector.segment("د. سارة استقبلت المريض."))
        assert len(result) == 1

    def test_arabic_terminator_cluster(self, ar_detector):
        """Multiple consecutive terminators should not produce interior splits."""
        result = list(ar_detector.segment("مرحباً!!!"))
        assert len(result) == 1

    def test_arabic_terminator_cluster_then_sentence(self, ar_detector):
        """After a terminator cluster, a new sentence should be detected."""
        result = list(ar_detector.segment("مرحباً!! منذ زمان."))
        assert len(result) == 2
        assert result[0] == "مرحباً!!"

    def test_arabic_common_sent_starters_split(self, ar_detector):
        """Common sentence starters like 'ولكن' should prompt a split."""
        result = list(ar_detector.segment("أمطرت طوال اليوم. ولكننا ذهبنا."))
        assert len(result) == 2

    def test_arabic_geopolitical_no_split(self, ar_detector):
        """Arabic geopolitical abbreviations should not cause mid-sentence splits."""
        result = list(ar_detector.segment("زار و.م.أ. الرئيس أوروبا."))
        assert len(result) == 1


# ---------------------------------------------------------------------------
# PtRules — new Portuguese rules
# ---------------------------------------------------------------------------


class TestPtRulesAttributes:
    def test_reference_abbrvs_excludes_no(self):
        """PtRules should remove 'no' from reference abbrvs (conflicts with Portuguese)."""
        assert "no" not in PtRules.REFERENCE_ABBRVS

    def test_reference_abbrvs_excludes_nos(self):
        """PtRules should remove 'nos' from reference abbrvs."""
        assert "nos" not in PtRules.REFERENCE_ABBRVS

    def test_reference_abbrvs_excludes_para(self):
        """PtRules should remove 'para' from reference abbrvs."""
        assert "para" not in PtRules.REFERENCE_ABBRVS

    def test_reference_abbrvs_adds_portuguese(self):
        """PtRules should add Portuguese-specific reference abbreviations."""
        assert "pág" in PtRules.REFERENCE_ABBRVS
        assert "pags" in PtRules.REFERENCE_ABBRVS
        assert "núm" in PtRules.REFERENCE_ABBRVS
        assert "nro" in PtRules.REFERENCE_ABBRVS

    def test_heading_tokens_extends_base(self):
        """PtRules.HEADING_TOKENS should include Portuguese headings."""
        assert "Capítulo" in PtRules.HEADING_TOKENS
        assert "Artigo" in PtRules.HEADING_TOKENS
        assert "Anexo" in PtRules.HEADING_TOKENS
        assert "Seção" in PtRules.HEADING_TOKENS

    def test_heading_tokens_inherits_base(self):
        """PtRules.HEADING_TOKENS should still contain base headings."""
        assert "Part" in PtRules.HEADING_TOKENS
        assert "Section" in PtRules.HEADING_TOKENS

    def test_mid_sentence_abbrvs_excludes_ave(self):
        """PtRules removes 'ave' from MID_SENTENCE_ABBRVS (uses 'av' instead)."""
        assert "ave" not in PtRules.MID_SENTENCE_ABBRVS

    def test_mid_sentence_abbrvs_adds_portuguese_streets(self):
        """PtRules should add Portuguese street abbreviations."""
        assert "av" in PtRules.MID_SENTENCE_ABBRVS
        assert "r" in PtRules.MID_SENTENCE_ABBRVS
        assert "al" in PtRules.MID_SENTENCE_ABBRVS
        assert "transv" in PtRules.MID_SENTENCE_ABBRVS

    def test_geopolitical_abbrvs_extends_base(self):
        """PtRules.GEOPOLITICAL_ABBRVS should include Portuguese-specific ones."""
        assert "E.U.A" in PtRules.GEOPOLITICAL_ABBRVS
        assert "U.E" in PtRules.GEOPOLITICAL_ABBRVS
        # Still inherits base
        assert "U.S" in PtRules.GEOPOLITICAL_ABBRVS

    def test_date_abbrvs_extends_base(self):
        """PtRules.DATE_ABBRVS should include Portuguese month/day abbreviations."""
        assert "fev" in PtRules.DATE_ABBRVS  # fevereiro
        assert "abr" in PtRules.DATE_ABBRVS  # abril
        assert "seg" in PtRules.DATE_ABBRVS  # segunda-feira
        assert "sáb" in PtRules.DATE_ABBRVS  # sábado

    def test_common_sent_starters(self):
        """PtRules.COMMON_SENT_STARTERS should include Portuguese articles and pronouns."""
        assert "O" in PtRules.COMMON_SENT_STARTERS
        assert "A" in PtRules.COMMON_SENT_STARTERS
        assert "Eu" in PtRules.COMMON_SENT_STARTERS
        assert "Contudo" in PtRules.COMMON_SENT_STARTERS

    def test_title_abbrvs_extends_base(self):
        """PtRules.TITLE_ABBRVS should add Portuguese professional titles."""
        assert "sr" in PtRules.TITLE_ABBRVS
        assert "sra" in PtRules.TITLE_ABBRVS
        assert "prof" in PtRules.TITLE_ABBRVS
        assert "eng" in PtRules.TITLE_ABBRVS


class TestPtRulesSegmentation:
    def test_portuguese_basic_split(self, pt_detector):
        """Standard Portuguese sentences should be split correctly."""
        result = list(pt_detector.segment("Olá mundo. Como estás? Bem, obrigado."))
        assert len(result) == 3

    def test_portuguese_title_no_split(self, pt_detector):
        """Portuguese title 'Sr.' should not create a sentence boundary."""
        result = list(pt_detector.segment("O Sr. Garcia chegou ontem. A Sra. Lopes também."))
        assert len(result) == 2
        assert result[0] == "O Sr. Garcia chegou ontem."

    def test_portuguese_page_abbr_no_split(self, pt_detector):
        """'pág.' followed by a number should not split."""
        result = list(pt_detector.segment("Veja-se a pág. 55 do livro."))
        assert len(result) == 1

    def test_portuguese_chapter_heading_no_split(self, pt_detector):
        """'Capítulo X.' should not produce an interior split."""
        text = "Capítulo 1. O Começo. Estava escuro lá fora."
        result = list(pt_detector.segment(text))
        assert result[0] == "Capítulo 1. O Começo."

    def test_portuguese_av_no_split(self, pt_detector):
        """'Av.' street abbreviation should not create a sentence boundary."""
        result = list(pt_detector.segment("Vive na Av. Sempre Viva."))
        assert len(result) == 1

    def test_portuguese_eua_no_split(self, pt_detector):
        """'E.U.A.' geopolitical abbreviation should not split mid-sentence."""
        result = list(pt_detector.segment("O presidente dos E.U.A. visitou a Europa."))
        assert len(result) == 1

    def test_portuguese_n_ordinal_no_split(self, pt_detector):
        """'n.º' ordinal indicator should not create a sentence boundary."""
        result = list(pt_detector.segment("A casa fica na Urb. Das Rosas, Lote A, n.º 15 do Bairro Social."))
        assert len(result) == 1

    def test_portuguese_date_abbr_no_split(self, pt_detector):
        """Portuguese date abbreviation 'abr.' followed by a year should not split."""
        result = list(pt_detector.segment("Nasceu a 5 de abr. de 1990."))
        assert len(result) == 1

    def test_portuguese_ellipsis_no_split(self, pt_detector):
        """Ellipsis should not cause a split in a Portuguese sentence."""
        result = list(pt_detector.segment("O projeto estava quase terminado... mas encontrámos um problema."))
        assert len(result) == 1

    def test_portuguese_r_street_no_split(self, pt_detector):
        """'R.' street abbreviation should not create a sentence boundary."""
        result = list(pt_detector.segment("Vivem na R. Direita, 12."))
        assert len(result) == 1

    def test_portuguese_no_not_treated_as_reference(self, pt_detector):
        """'no' should not be treated as a reference abbreviation (was removed)."""
        # "não" → "não." should end the sentence correctly
        result = list(pt_detector.segment("Ontem disse-lhe que não. 5 pessoas chegaram depois."))
        assert len(result) == 2


# ---------------------------------------------------------------------------
# RuRules — new Russian rules
# ---------------------------------------------------------------------------


class TestRuRulesAttributes:
    def test_geopolitical_abbrvs_empty(self):
        """RuRules.GEOPOLITICAL_ABBRVS should be an empty set."""
        assert RuRules.GEOPOLITICAL_ABBRVS == set()

    def test_quotative_particles_empty(self):
        """RuRules.QUOTATIVE_PARTICLES should be an empty set."""
        assert RuRules.QUOTATIVE_PARTICLES == set()

    def test_title_abbrvs_russian(self):
        """RuRules.TITLE_ABBRVS should contain Russian-specific titles."""
        assert "проф" in RuRules.TITLE_ABBRVS
        assert "д-р" in RuRules.TITLE_ABBRVS
        assert "акад" in RuRules.TITLE_ABBRVS
        assert "г-н" in RuRules.TITLE_ABBRVS
        assert "г-жа" in RuRules.TITLE_ABBRVS

    def test_title_abbrvs_military_russian(self):
        """RuRules.TITLE_ABBRVS should contain Russian military titles."""
        assert "ген" in RuRules.TITLE_ABBRVS
        assert "полк" in RuRules.TITLE_ABBRVS
        assert "лейт" in RuRules.TITLE_ABBRVS

    def test_reference_abbrvs_russian(self):
        """RuRules.REFERENCE_ABBRVS should contain Russian reference abbreviations."""
        assert "см" in RuRules.REFERENCE_ABBRVS
        assert "стр" in RuRules.REFERENCE_ABBRVS
        assert "табл" in RuRules.REFERENCE_ABBRVS
        assert "рис" in RuRules.REFERENCE_ABBRVS

    def test_reference_abbrvs_has_section_symbol(self):
        """'§' should be in RuRules.REFERENCE_ABBRVS."""
        assert "§" in RuRules.REFERENCE_ABBRVS

    def test_mid_sentence_abbrvs_extends_base(self):
        """RuRules.MID_SENTENCE_ABBRVS should include Russian date/unit abbreviations."""
        assert "г" in RuRules.MID_SENTENCE_ABBRVS
        assert "гг" in RuRules.MID_SENTENCE_ABBRVS
        assert "руб" in RuRules.MID_SENTENCE_ABBRVS
        assert "тыс" in RuRules.MID_SENTENCE_ABBRVS
        assert "и т.д" in RuRules.MID_SENTENCE_ABBRVS

    def test_names_with_exclamation_russian(self):
        """RuRules should extend base NAMES_WITH_EXCLAMATION with Russian brands."""
        assert "Яндекс" in RuRules.NAMES_WITH_EXCLAMATION
        assert "Билайн" in RuRules.NAMES_WITH_EXCLAMATION
        assert "Сбер" in RuRules.NAMES_WITH_EXCLAMATION

    def test_names_with_exclamation_inherits_base(self):
        """RuRules should still contain base NAMES_WITH_EXCLAMATION entries."""
        assert "Yahoo" in RuRules.NAMES_WITH_EXCLAMATION

    def test_heading_tokens_russian(self):
        """RuRules.HEADING_TOKENS should contain Russian structural headings."""
        assert "Глава" in RuRules.HEADING_TOKENS
        assert "Часть" in RuRules.HEADING_TOKENS
        assert "Раздел" in RuRules.HEADING_TOKENS

    def test_common_sent_starters_russian(self):
        """RuRules.COMMON_SENT_STARTERS should contain Russian transition words."""
        assert "Однако" in RuRules.COMMON_SENT_STARTERS
        assert "Следовательно" in RuRules.COMMON_SENT_STARTERS
        assert "Я" in RuRules.COMMON_SENT_STARTERS

    def test_date_abbrvs_russian(self):
        """RuRules.DATE_ABBRVS should contain Russian month abbreviations."""
        assert "янв" in RuRules.DATE_ABBRVS
        assert "фев" in RuRules.DATE_ABBRVS
        assert "мар" in RuRules.DATE_ABBRVS
        assert "пн" in RuRules.DATE_ABBRVS


class TestRuRulesSegmentation:
    def test_russian_basic_split(self, ru_detector):
        """Standard Russian sentences should be split correctly."""
        result = list(ru_detector.segment("Привет мир. Как дела? Хорошо, спасибо."))
        assert len(result) == 3

    def test_russian_title_no_split(self, ru_detector):
        """Russian title 'Проф.' should not create a sentence boundary."""
        result = list(ru_detector.segment("Проф. Иванов прочитал лекцию."))
        assert len(result) == 1

    def test_russian_dr_title_no_split(self, ru_detector):
        """Russian 'Д-р' should not create a sentence boundary."""
        result = list(ru_detector.segment("Д-р Смирнов принял пациента."))
        assert len(result) == 1

    def test_russian_reference_see_no_split(self, ru_detector):
        """'См.' reference abbreviation should not split."""
        result = list(ru_detector.segment("См. главу 3 в т. 2."))
        assert len(result) == 1

    def test_russian_chapter_heading_no_split(self, ru_detector):
        """'Глава X.' heading should not produce an interior split."""
        text = "Глава 1. Начало. В комнате было темно и тихо."
        result = list(ru_detector.segment(text))
        assert result[0] == "Глава 1. Начало."

    def test_russian_terminator_cluster(self, ru_detector):
        """Multiple consecutive terminators should not produce interior splits."""
        result = list(ru_detector.segment("Привет!!!"))
        assert len(result) == 1

    def test_russian_terminator_cluster_then_sentence(self, ru_detector):
        """After a cluster !!, a new sentence should be detected."""
        result = list(ru_detector.segment("Привет!! Давно не виделись."))
        assert len(result) == 2

    def test_russian_initials_no_split(self, ru_detector):
        """Russian initials like 'И.' should not split in 'Иван И. Петров'."""
        result = list(ru_detector.segment("Меня зовут Иван И. Петров."))
        assert len(result) == 1

    def test_russian_date_abbr_followed_by_number(self, ru_detector):
        """Russian date abbreviation 'пн.' followed by a number should not split."""
        result = list(ru_detector.segment("Встреча назначена на пн. 15 января."))
        assert len(result) == 1

    def test_russian_latin_geopolitical_not_suppressed(self, ru_detector):
        """Since GEOPOLITICAL_ABBRVS is empty, Latin geo abbrevs may split normally."""
        # RuRules has empty GEOPOLITICAL_ABBRVS so no special treatment for U.S., etc.
        # This is intentional per the rule comment in ru.py
        assert RuRules.GEOPOLITICAL_ABBRVS == set()


# ---------------------------------------------------------------------------
# ZhRules — new Chinese rules
# ---------------------------------------------------------------------------


class TestZhRulesAttributes:
    def test_quotative_particles(self):
        """ZhRules.QUOTATIVE_PARTICLES should be exactly {'如是'}."""
        assert ZhRules.QUOTATIVE_PARTICLES == {"如是"}

    def test_reporting_words_chinese(self):
        """ZhRules.REPORTING_WORDS should contain common Chinese speech verbs."""
        assert "说" in ZhRules.REPORTING_WORDS
        assert "道" in ZhRules.REPORTING_WORDS
        assert "表示" in ZhRules.REPORTING_WORDS
        assert "指出" in ZhRules.REPORTING_WORDS
        assert "认为" in ZhRules.REPORTING_WORDS

    def test_names_with_exclamation_extends_base(self):
        """ZhRules should add Chinese anime/media names to NAMES_WITH_EXCLAMATION."""
        assert "排球少年！" in ZhRules.NAMES_WITH_EXCLAMATION
        assert "总之就是非常可爱" in ZhRules.NAMES_WITH_EXCLAMATION
        assert "轻音少女" in ZhRules.NAMES_WITH_EXCLAMATION

    def test_names_with_exclamation_inherits_base(self):
        """ZhRules should still contain base entries in NAMES_WITH_EXCLAMATION."""
        assert "Yahoo" in ZhRules.NAMES_WITH_EXCLAMATION

    def test_fullwidth_latin_pattern_in_mid_sentence_finders(self, zh_rules):
        """The fullwidth latin letter pattern should be in MID_SENTENCE_FINDER_LST."""
        patterns = [p.pattern for p in ZhRules.MID_SENTENCE_FINDER_LST]
        assert any(r"\uFF21" in pat or "FF21" in pat for pat in patterns), (
            "Expected fullwidth letter pattern in ZhRules.MID_SENTENCE_FINDER_LST"
        )


class TestZhRulesSegmentation:
    def test_chinese_period_splits(self, zh_detector):
        """Chinese ideographic period '。' should split sentences."""
        result = list(zh_detector.segment("你好世界。 你好吗？"))
        assert len(result) == 2

    def test_chinese_question_mark_splits(self, zh_detector):
        """'？' should split Chinese sentences."""
        result = list(zh_detector.segment("你叫什么名字？ 我叫张三。"))
        assert len(result) == 2

    def test_chinese_fullwidth_us_no_split(self, zh_detector):
        """Fullwidth 'Ｕ．Ｓ．Ａ．' should not cause a mid-sentence split."""
        result = list(zh_detector.segment("Ｕ．Ｓ．Ａ．的经济政策非常复杂。 下个月的动向值得关注。"))
        assert len(result) == 2
        assert "Ｕ．Ｓ．Ａ．的经济政策非常复杂。" in result[0]

    def test_chinese_fullwidth_eu_no_split(self, zh_detector):
        """Fullwidth 'Ｅ．Ｕ．' should not split mid-sentence."""
        result = list(zh_detector.segment("Ｅ．Ｕ．发布了新的法规。 企业需要遵守。"))
        assert len(result) == 2

    def test_chinese_quotative_particle_no_split(self, zh_detector):
        """'如是' quotative particle should suppress a boundary after closing quote."""
        result = list(zh_detector.segment("嫌疑人表示「我没有做过」如是供述。 警方继续调查。"))
        assert len(result) == 2
        assert result[0] == "嫌疑人表示「我没有做过」如是供述。"

    def test_chinese_reporting_word_no_split(self, zh_detector):
        """Chinese reporting words like '说道' should suppress splits after quotes."""
        result = list(zh_detector.segment("「不可能吧，」他说道。 但是没人相信他。"))
        assert len(result) == 2
        assert result[0] == "「不可能吧，」他说道。"


# ---------------------------------------------------------------------------
# JaRules — modified Japanese rules
# ---------------------------------------------------------------------------


class TestJaRulesModifications:
    def test_case_markers_not_in_own_dict(self):
        """CASE_MARKERS was removed from JaRules in this PR; should fall back to base."""
        assert "CASE_MARKERS" not in JaRules.__dict__, (
            "JaRules should not define CASE_MARKERS; it was removed in this PR"
        )

    def test_case_markers_falls_back_to_base_empty(self, ja_rules):
        """JaRules should inherit the empty CASE_MARKERS from base Rules."""
        assert ja_rules.CASE_MARKERS == set()

    def test_geopolitical_abbrvs_not_fullwidth(self):
        """JaRules should no longer use FULLWIDTH_GEOPOLITICAL_ABBRVS."""
        # After the PR, JaRules uses default Rules.GEOPOLITICAL_ABBRVS (ASCII-based)
        # not the removed FULLWIDTH_GEOPOLITICAL_ABBRVS constant
        import yasbd.rules.base as base_module

        assert not hasattr(base_module, "FULLWIDTH_GEOPOLITICAL_ABBRVS")
        # JaRules should not have its own GEOPOLITICAL_ABBRVS (removed in PR)
        assert "GEOPOLITICAL_ABBRVS" not in JaRules.__dict__, (
            "JaRules no longer overrides GEOPOLITICAL_ABBRVS (PR change)"
        )

    def test_fullwidth_pattern_in_mid_sentence_finders(self, ja_rules):
        """JaRules._compile_regex_dynamically should add the fullwidth pattern."""
        patterns = [p.pattern for p in JaRules.MID_SENTENCE_FINDER_LST]
        assert any(r"\uFF21" in pat or "FF21" in pat for pat in patterns), (
            "Expected fullwidth letter pattern in JaRules.MID_SENTENCE_FINDER_LST"
        )

    def test_fullwidth_pattern_covers_both_cases(self, ja_rules):
        """The fullwidth pattern should cover uppercase (FF21-FF3A) and lowercase (FF41-FF5A)."""
        patterns = [p.pattern for p in JaRules.MID_SENTENCE_FINDER_LST]
        fullwidth_pattern = next(
            (p for p in patterns if "FF21" in p or r"\uFF21" in p), None
        )
        assert fullwidth_pattern is not None
        assert "FF3A" in fullwidth_pattern or r"\uFF3A" in fullwidth_pattern
        assert "FF41" in fullwidth_pattern or r"\uFF41" in fullwidth_pattern


# ---------------------------------------------------------------------------
# Regression / boundary cases
# ---------------------------------------------------------------------------


class TestRegressionCases:
    """Edge cases and regression tests for changes introduced in this PR."""

    def test_base_no_fullwidth_constant(self):
        """Importing FULLWIDTH_GEOPOLITICAL_ABBRVS from base should raise ImportError."""
        with pytest.raises(ImportError):
            from yasbd.rules.base import FULLWIDTH_GEOPOLITICAL_ABBRVS  # noqa: F401

    def test_ar_rules_regex_cached_per_class(self):
        """ArRules regex caching should be isolated from the base Rules cache."""
        Rules._REGEX_CACHED = False
        ArRules._REGEX_CACHED = False

        _ = Rules()
        ar = ArRules()
        assert "NAIVE_BOUNDARY_FINDER" in type(ar).__dict__, (
            "ArRules should have its own compiled NAIVE_BOUNDARY_FINDER"
        )

    def test_zh_rules_regex_cached_per_class(self):
        """ZhRules regex caching should be isolated from other classes."""
        ZhRules._REGEX_CACHED = False
        zh = ZhRules()
        assert "MID_SENTENCE_FINDER_LST" in type(zh).__dict__, (
            "ZhRules should have its own MID_SENTENCE_FINDER_LST"
        )

    def test_pt_rules_reference_set_subtraction_is_correct(self):
        """PtRules REFERENCE_ABBRVS should be (base - removed) | added, not just additive."""
        # Verify the set difference was applied
        assert "no" in Rules.REFERENCE_ABBRVS, "base should still have 'no'"
        assert "no" not in PtRules.REFERENCE_ABBRVS, "PtRules should have removed 'no'"

    def test_pt_rules_mid_sentence_set_subtraction_is_correct(self):
        """PtRules MID_SENTENCE_ABBRVS should have removed 'ave'."""
        assert "ave" in Rules.MID_SENTENCE_ABBRVS, "base should have 'ave'"
        assert "ave" not in PtRules.MID_SENTENCE_ABBRVS, "PtRules should have removed 'ave'"

    def test_ru_rules_empty_geopolitical_does_not_break_regex(self):
        """Empty GEOPOLITICAL_ABBRVS should still compile regex without error."""
        RuRules._REGEX_CACHED = False
        try:
            ru = RuRules()
            _ = ru.NAIVE_BOUNDARY_FINDER
        except Exception as e:
            pytest.fail(f"RuRules regex compilation failed with empty GEOPOLITICAL_ABBRVS: {e}")

    def test_superscript_indicator_pattern_matches_correctly(self):
        """The \.(?=[ºª]) pattern should match a dot before ordinal superscript."""
        # Find the pattern in base rules
        Rules._REGEX_CACHED = False
        rules = Rules()
        superscript_pats = [
            p for p in rules.MID_SENTENCE_FINDER_LST
            if hasattr(p, "pattern") and r"(?=[ºª])" in p.pattern
        ]
        assert superscript_pats, "No superscript indicator pattern found"
        pat = superscript_pats[0]
        # Should match "n.º" at the dot
        assert pat.search("n.º"), "Pattern should match dot before º"
        assert pat.search("1.ª"), "Pattern should match dot before ª"
        # Should not match plain dots
        assert not pat.search("end."), "Pattern should not match terminal dot"

    def test_ar_rules_terminators_superset(self):
        """Arabic terminators should be strictly larger than base terminators."""
        assert len(ArRules.TERMINATORS) > len(Rules.TERMINATORS)
        assert "؟" in ArRules.TERMINATORS
        assert "؟" not in Rules.TERMINATORS

    def test_zh_rules_has_more_mid_sentence_finders_than_base(self):
        """ZhRules should have more MID_SENTENCE_FINDER_LST entries than base."""
        ZhRules._REGEX_CACHED = False
        ZhRules()
        Rules._REGEX_CACHED = False
        Rules()
        assert len(ZhRules.MID_SENTENCE_FINDER_LST) > len(Rules.MID_SENTENCE_FINDER_LST), (
            "ZhRules should add at least the fullwidth pattern"
        )

    def test_ar_rules_has_more_mid_sentence_finders_than_base(self):
        """ArRules should have more MID_SENTENCE_FINDER_LST entries than base."""
        ArRules._REGEX_CACHED = False
        ArRules()
        Rules._REGEX_CACHED = False
        Rules()
        assert len(ArRules.MID_SENTENCE_FINDER_LST) > len(Rules.MID_SENTENCE_FINDER_LST), (
            "ArRules should add at least the ellipsis pattern"
        )

    def test_new_languages_loadable_via_boundary_detector(self):
        """BoundaryDetector should successfully load all new language modules."""
        for lang in ("ar", "pt", "ru", "zh"):
            try:
                det = BoundaryDetector(lang=lang)
                assert det.lang == lang
            except ValueError:
                pytest.fail(f"BoundaryDetector could not load lang={lang!r}")

    def test_new_languages_segment_single_sentence(self):
        """Each new language should correctly segment a trivial single sentence."""
        cases = {
            "ar": ("مرحباً بالعالم.", ["مرحباً بالعالم."]),
            "pt": ("Olá mundo.", ["Olá mundo."]),
            "ru": ("Привет мир.", ["Привет мир."]),
            "zh": ("你好世界。", ["你好世界。"]),
        }
        for lang, (text, expected) in cases.items():
            det = BoundaryDetector(lang=lang)
            result = list(det.segment(text))
            assert result == expected, f"lang={lang}: got {result!r}, expected {expected!r}"
