class YasbdError(Exception):
    """Base exception for all yasbd errors."""


class UnsupportedLanguageError(YasbdError, ValueError):
    """Raised when an unsupported language code is provided."""


class InvalidInputError(YasbdError, TypeError):
    """Raised when invalid input(s) are encountered."""


class CleanStepError(YasbdError, TypeError):
    """Raised when a StreamCleaner extra step fails (non-callable or non-str return)."""
