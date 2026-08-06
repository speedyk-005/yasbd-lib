import io

from yasbd.utils.cleaner import StreamCleaner, normalize_newlines


def test_normalize_newlines_windows():
    """Verify Windows (\\r\\n) line endings are normalized to \\n."""
    assert normalize_newlines("hello\r\nworld") == "hello\nworld"
    assert normalize_newlines("line1\r\nline2\r\nline3") == "line1\nline2\nline3"


def test_normalize_newlines_mac():
    """Verify Classic Mac (\\r) line endings are normalized to \\n."""
    assert normalize_newlines("hello\rworld") == "hello\nworld"
    assert normalize_newlines("line1\rline2\rline3") == "line1\nline2\nline3"


def test_normalize_newlines_unix():
    """Verify Unix (\\n) line endings remain unchanged."""
    assert normalize_newlines("hello\nworld") == "hello\nworld"
    assert normalize_newlines("line1\nline2\nline3") == "line1\nline2\nline3"


def test_normalize_newlines_mixed():
    """Verify mixed line endings are all normalized to \\n."""
    assert (
        normalize_newlines("line1\r\nline2\rline3\nline4")
        == "line1\nline2\nline3\nline4"
    )


def test_stream_cleaner_with_different_line_endings():
    """Verify StreamCleaner normalizes line endings across inputs."""
    windows_cleaner = StreamCleaner("Hello.\r\nWorld")
    assert list(windows_cleaner) == ["Hello.\nWorld"]

    mac_cleaner = StreamCleaner("Hello.\rWorld")
    assert list(mac_cleaner) == ["Hello.\nWorld"]

    unix_cleaner = StreamCleaner("Hello.\nWorld")
    assert list(unix_cleaner) == ["Hello.\nWorld"]


def test_stream_cleaner_skip_normalize_newlines():
    """Verify normalize_newlines step can be skipped via steps_to_skip."""
    cleaner = StreamCleaner(
        io.StringIO("hello.\rworld", newline=""),
        steps_to_skip=["normalize_newlines", "fix_mojibake", "fix_ocr_text"],
    )
    assert list(cleaner) == ["hello.\rworld"]
