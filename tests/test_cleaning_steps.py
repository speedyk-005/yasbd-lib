import pytest

from yasbd.utils.cleaner import normalize_newlines, normalize_slashes, normalize_spaces, unwrap_htmls


class TestUnwrapHtmls:
    """Tests for unwrap_htmls named function."""

    def test_no_html_tags(self):
        """Text without HTML tags should pass through unchanged."""
        result = unwrap_htmls("Hello world, this is plain text.")
        assert result == "Hello world, this is plain text."

    def test_removes_script_tag(self):
        """Script tags and their content should be removed."""
        result = unwrap_htmls("Before<script>alert('xss')</script>After")
        assert result == "BeforeAfter"

    def test_removes_style_tag(self):
        """Style tags and their content should be removed."""
        result = unwrap_htmls("Text<style>.hidden{color:red}</style>More text")
        assert result =="TextMore text"

    def test_removes_iframe_tag(self):
        """Iframe tags and their content should be removed."""
        result = unwrap_htmls("Start<iframe src='url'></iframe>End")
        assert result == "StartEnd"

    def test_preserves_safe_html(self):
        """Lightweight formatting tags should be preserved."""
        result = unwrap_htmls("<b>Bold</b> and <i>italic</i>")
        assert result == "<b>Bold</b> and <i>italic</i>"

    def test_empty_string(self):
        """Empty string should return empty string."""
        result = unwrap_htmls("")
        assert result == ""

    def test_only_html_tags(self):
        """String with only tags should return empty string."""
        result = unwrap_htmls("<script>only</script>")
        assert result == ""

    def test_guarded_path_no_less_than(self):
        """Guarded path: text without '<' character."""
        result = unwrap_htmls("5 < 10 and 10 > 5")
        assert result == "5 < 10 and 10 > 5"


class TestNormalizeSlashes:
    """Tests for normalize_slashes named function."""

    def test_no_trailing_slashes(self):
        """Text without triple slashes should pass through unchanged."""
        result = normalize_slashes("path/to/file")
        assert result == "path/to/file"

    def test_removes_triple_slashes(self):
        """Triple slashes should be removed entirely."""
        result = normalize_slashes("path///to///file")
        assert result == "pathtofile"

    def test_preserves_double_slashes(self):
        """Double slashes (e.g., URLs) should be preserved."""
        result = normalize_slashes("https://example.com")
        assert result == "https://example.com"

    def test_single_slashes_unchanged(self):
        """Single slashes should remain unchanged."""
        result = normalize_slashes("a/b/c")
        assert result == "a/b/c"

    def test_empty_string(self):
        """Empty string should return empty string."""
        result = normalize_slashes("")
        assert result == ""

    def test_only_slashes(self):
        """String of triple slashes should become empty string."""
        result = normalize_slashes("///")
        assert result == ""

    def test_guarded_path_no_triple_slashes(self):
        """Guarded path: text without '///'."""
        result = normalize_slashes("C:/Users/name/path")
        assert result == "C:/Users/name/path"


class TestNormalizeSpaces:
    """Tests for normalize_spaces named function."""

    def test_no_multiple_spaces(self):
        """Text without multiple spaces should pass through unchanged."""
        result = normalize_spaces("Hello world")
        assert result == "Hello world"

    def test_reduces_multiple_spaces(self):
        """Multiple consecutive spaces should be reduced to single space."""
        result = normalize_spaces("Hello    world")
        assert result =="Hello world"

    def test_preserves_single_spaces(self):
        """Single spaces between words should be preserved."""
        result = normalize_spaces("Hello   world   test")
        assert result == "Hello world test"

    def test_leading_trailing_space(self):
        """Leading and trailing spaces are also normalized internally."""
        result = normalize_spaces("  Hello world  ")
        assert result == " Hello world "

    def test_empty_string(self):
        """Empty string should return empty string."""
        result = normalize_spaces("")
        assert result == ""

    def test_all_spaces(self):
        """String of multiple spaces should become single space."""
        result = normalize_spaces("     ")
        assert result == " "


class TestNormalizeNewlines:
    """Tests for normalize_newlines named function."""

    def test_windows_newlines(self):
        """Windows \\r\\n line endings should be normalized to \\n."""
        result = normalize_newlines("Hello\r\nWorld")
        assert result == "Hello\nWorld"

    def test_mac_newlines(self):
        """Classic Mac \\r line endings should be normalized to \\n."""
        result = normalize_newlines("Hello\rWorld")
        assert result == "Hello\nWorld"

    def test_unix_newlines(self):
        """Unix \\n line endings should remain unchanged."""
        result = normalize_newlines("Hello\nWorld")
        assert result == "Hello\nWorld"

    def test_mixed_newlines(self):
        """Mixed line endings should be normalized consistently."""
        result = normalize_newlines("Line1\r\nLine2\rLine3\nLine4")
        assert result == "Line1\nLine2\nLine3\nLine4"

    def test_empty_string(self):
        """Empty string should return empty string."""
        result = normalize_newlines("")
        assert result == ""

    def test_no_newlines(self):
        """String without newlines should pass through unchanged."""
        result = normalize_newlines("Hello world")
        assert result == "Hello world"

    def test_only_newlines(self):
        """String with only line endings should be normalized."""
        result = normalize_newlines("\r\n\r\n\r\n")
        assert result == "\n\n\n"

    def test_guarded_path_no_carriage_returns(self):
        """Guarded path: text without \\r or \\r\\n."""
        result = normalize_newlines("No weird newlines here")
        assert result == "No weird newlines here"