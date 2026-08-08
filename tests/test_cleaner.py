import io

from yasbd.utils.cleaner import (
    StreamCleaner,
    normalize_newlines,
    unwrap_htmls,
    normalize_slashes,
    normalize_spaces,
)


def test_normalize_newlines_windows():
    """Verify Windows (\r\n) line endings are normalized to \n."""
    assert normalize_newlines("hello\r\nworld") == "hello\nworld"
    assert normalize_newlines("line1\r\nline2\r\nline3") == "line1\nline2\nline3"


def test_normalize_newlines_mac():
    """Verify Classic Mac (\r) line endings are normalized to \n."""
    assert normalize_newlines("hello\rworld") == "hello\nworld"
    assert normalize_newlines("line1\rline2\rline3") == "line1\nline2\nline3"


def test_normalize_newlines_unix():
    """Verify Unix (\n) line endings remain unchanged."""
    assert normalize_newlines("hello\nworld") == "hello\nworld"
    assert normalize_newlines("line1\nline2\nline3") == "line1\nline2\nline3"


def test_normalize_newlines_mixed():
    """Verify mixed line endings are all normalized to \n."""
    assert (
        normalize_newlines("line1\r\nline2\rline3\nline4")
        == "line1\nline2\nline3\nline4"
    )


def test_stream_cleaner_skip_normalize_newlines():
    """Verify normalize_newlines step can be skipped via steps_to_skip."""
    cleaner = StreamCleaner(
        io.StringIO("hello.\rworld", newline=""),
        steps_to_skip=["normalize_newlines", "fix_mojibake", "fix_ocr_text"],
    )
    assert list(cleaner) == ["hello.\rworld"]


def test_unwrap_htmls_removes_html_tags():
    """Verify unwrap_htmls removes HTML tags and comments."""
    assert unwrap_htmls("<p>Hello</p>") == "Hello"
    assert unwrap_htmls("<!-- comment -->Hello") == "Hello"
    # <b>, <i>, <u> are preserved as lightweight formatting
    assert unwrap_htmls("Hello <b>world</b>!") == "Hello <b>world</b>!"
    assert unwrap_htmls("Hello <i>world</i>!") == "Hello <i>world</i>!"
    assert unwrap_htmls("Hello <u>world</u>!") == "Hello <u>world</u>!"
    assert unwrap_htmls("Hello world") == "Hello world"
    assert unwrap_htmls("") == ""
    assert unwrap_htmls("<script>alert('xss')</script>") == ""


def test_unwrap_htmls_guarded_paths():
    """Verify unwrap_htmls handles both guarded and unguarded paths."""
    # Guarded path: text without '<' returns unchanged
    assert unwrap_htmls("no html here") == "no html here"
    # Unguarded path: text with '<' gets processed
    assert unwrap_htmls("<p>paragraph</p>") == "paragraph"


def test_normalize_slashes_replaces_triple_slashes():
    """Verify normalize_slashes replaces triple consecutive forward slashes with empty string."""
    assert normalize_slashes("text///with///slashes") == "textwithslashes"
    assert normalize_slashes("text///") == "text"
    assert normalize_slashes("text") == "text"
    assert normalize_slashes("///") == ""
    assert normalize_slashes("a///b///c") == "abc"


def test_normalize_slashes_guarded_and_unguarded():
    """Verify normalize_slashes handles both guarded and unguarded paths."""
    # Guarded: no triple slashes
    assert normalize_slashes("a/b/c") == "a/b/c"
    assert normalize_slashes("no slashes") == "no slashes"
    # Unguarded: has triple slashes
    assert normalize_slashes("a///b") == "ab"
    assert normalize_slashes("start///end") == "startend"


def test_normalize_spaces_replaces_multiple_spaces():
    """Verify normalize_spaces replaces multiple consecutive spaces."""
    assert normalize_spaces("hello  world") == "hello world"
    assert normalize_spaces("hello   world") == "hello world"
    assert normalize_spaces("hello  world  test") == "hello world test"
    assert normalize_spaces("  leading") == " leading"
    assert normalize_spaces("trailing  ") == "trailing "
    assert normalize_spaces("") == ""
    assert normalize_spaces(" ") == " "


def test_normalize_spaces_guarded_and_unguarded():
    """Verify normalize_spaces handles both guarded and unguarded paths."""
    # Guarded: no multiple consecutive spaces
    assert normalize_spaces("hello world") == "hello world"
    assert normalize_spaces("single space") == "single space"
    # Unguarded: has multiple consecutive spaces
    assert normalize_spaces("hello  world") == "hello world"
    assert normalize_spaces("a   b") == "a b"


def test_cleaner_pipeline_integration():
    """Verify the full pipeline works with the new named functions."""
    # Test normalize_newlines with punctuation (not between word chars)
    cleaner = StreamCleaner("Hello.\r\nWorld")
    assert list(cleaner) == ["Hello.\nWorld"]

    # Test unwrap_htmls
    cleaner = StreamCleaner("<p>Hello</p>")
    assert list(cleaner) == ["Hello"]

    # Test normalize_slashes
    cleaner = StreamCleaner("test///value")
    assert list(cleaner) == ["testvalue"]

    # Test normalize_spaces
    cleaner = StreamCleaner("hello  world")
    assert list(cleaner) == ["hello world"]

    # Test combined: HTML with spaces and slashes
    cleaner = StreamCleaner("  <p>test  ///  value</p>  ")
    result = list(cleaner)[0]
    assert result == "test value"
