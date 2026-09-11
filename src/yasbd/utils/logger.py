import sys
from datetime import datetime

GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def log_info(verbose: bool, message: str, *args, **kwargs) -> None:
    """Log an info message if verbose is enabled.

    This is a convenience function that only logs when verbose mode is enabled,
    avoiding unnecessary log output in production.

    Args:
        verbose: If True, logs the message; if False, does nothing.
        *args: Positional arguments passed to logger.info().
        **kwargs: Keyword arguments passed to logger.info().

    Example:
        >>> log_info(True, "hello {}", "world")  # doctest: +ELLIPSIS
        \033...-... - hello world

        >>> log_info(False, "This will not be logged")
    """
    if not verbose:
        return

    frame = sys._getframe(1)  # noqa: SLF001

    module = frame.f_globals.get("__name__", "__main__")
    function = frame.f_code.co_name
    line = frame.f_lineno

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    message = message.format(*args, **kwargs)

    print(f"{GREEN}{now}{RESET} | {CYAN}{module}:{function}:{line}{RESET} - {message}")
