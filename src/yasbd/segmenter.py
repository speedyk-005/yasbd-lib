from collections.abc import Generator

from loguru import logger


class Span:
	def __init__(self, start: int, end: int, text: str):
		self.start = start
		self.end = end
		self.text = text


class Segmenter:
	def __init__(
		self,
		lang: str = "en",
		*,
		should_clean: bool = False,
		include_char_span: bool = False,
		skip_quote_and_paren: bool = False,
		verbose: bool = False,
	):
		self.lang = lang
		self.should_clean = should_clean
		self.include_char_span = include_char_span
		self.skip_quote_and_paren = skip_quote_and_paren
		self.verbose = verbose

	def segment(self, text: str) -> Generator[str | Span, None, None]:
		if not text.strip():
			if self.verbose:
				logger.info("Input text is empty. Returns empty result")
			return