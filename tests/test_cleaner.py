import pytest

from yasbd.utils.cleaner import clean_input


@pytest.mark.parametrize("input_text,removed", [
    (["<b>hello</b> world"], ["<b>", "</b>"]),
    (["text with <font color=red>red</font>"], ["<font", "</font>"]),
    (["<script>alert(1)</script>clean"], ["<script>", "</script>", "alert(1)"]),
    (["<style>.cls{}</style>keep"], ["<style>", "</style>", ".cls{}"]),
    (["<span>span</span> and <del>del</del>"], ["<span>", "</span>", "<del>", "</del>"]),
    (["{b^>inline<b^} formatting"], ["{b^>", "<b^}"]),
    (["three///slashes"], ["///"]),
    (["text &lt;script&gt;evil"], ["&lt;", "&gt;"]),
    (["42", "content"], ["42"]),
    (["x", "content after"], ["x"]),
    (["Page 1 of 10", "content"], ["Page 1 of 10"]),
    ([" 42 ", "content"], ["42"]),
    (["- 42 -", "content"], ["42"]),
    (["| Page 5 |", "text"], ["| Page 5 |"]),
    (["hello '' world"], ["''"]),
    (["hello   world"], ["  "]),
    (["line one\n. line two"], ["\n"]),
])
def test_text_cleanup(input_text, removed):
    cleaned = " ".join(clean_input(input_text))
    assert all(kw not in cleaned for kw in removed)
