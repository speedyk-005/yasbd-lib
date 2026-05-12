import io
from collections.abc import Generator
from importlib import import_module
from typing import NamedTuple

from loguru import logger


class TextSpan(NamedTuple):
	start: int
	end: int
	text: str

	@property
	def sent(self) -> str:
		"""Alias for pysbd compatibility"""
		return self.text

	def __str__(self) -> str:
		return f"[{self.start}:{self.end}] {self.text}"

	def __eq__(self, other) -> bool:
		if (
			isinstance(other, TextSpan)
			or hasattr(other, "sent") and hasattr(other, "start") and hasattr(other, "end")
		):
			return (self.start, self.end, self.sent) == (other.start, other.end, other.sent)
		return NotImplemented


class Segmenter:
	def __init__(
		self,
		lang: str = "en",
		*,
		should_clean: bool = False,
		include_char_span: bool = False,
		preserve_quote_and_paren: bool = False,
		verbose: bool = False,
	):
		self.lang = lang
		self.should_clean = should_clean
		self.include_char_span = include_char_span
		self.preserve_quote_and_paren = preserve_quote_and_paren
		self.verbose = verbose

		rule_module = import_module(f"yasbd.rules.{lang}_rule")
		self._rule = getattr(rule_module, f"{lang.capitalize()}Rule")() 

	def segment(self, input: str | io.IOBase) -> Generator[str | TextSpan, None, None]:
		if self._is_empty(input):
			if self.verbose:
				logger.info("Input is empty. Returns empty result")
			return
		
		for sent, span in self._rule.apply(input, self.preserve_quote_and_paren):
			if self.should_clean:
				stripped_sent = sent.strip()
				if stripped_sent:
					yield (
						TextSpan(start=span[0], end=span[1], text=stripped_sent)
						if self.include_char_span else stripped_sent
					)
			else:
				yield (
					TextSpan(start=span[0], end=span[1], text=sent)
					if self.include_char_span else sent
				)


	def _is_empty(self, input):
	    if isinstance(input, str):
	        return not input.strip()
	    
	    # Stream object
	    curr = input.tell()
	    exists = bool(input.read(1))
	    input.seek(curr)
	    return not exists

	def _wrap_as_span_obj(self, text: str, span: tuple) -> TextSpan:
		return 
