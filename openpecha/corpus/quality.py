# OpenPecha Toolkit: Corpus Quality Utility Functions
#
# Copyright (C) 2019-2022 NLTK Project
# Author: Edward Loper <edloper@gmail.com>
# URL: <https://www.nltk.org/>
# For license information, see LICENSE.TXT

from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from queue import Empty
from typing import Dict

from botok import WordTokenizer
from botok.vars import WordMarkers


class NonWordsCounter:
    """
    Class to count non words and it's ratio
    """

    def __init__(
        self,
        text: str = None,
        tokenizer: WordTokenizer = None,
        total_tokens: int = 0,
        total_non_words: int = 0,
        empty=False,
    ):
        self.total_tokens: int = total_tokens
        self.total_non_words: int = total_non_words
        if not total_non_words and not empty:
            self.count(text, tokenizer)

    def count(self, text, tokenizer):
        if not text:
            raise ValueError("required text input")
        tokenizer = tokenizer if tokenizer else WordTokenizer()
        tokens = tokenizer.tokenize(text)
        self.total_tokens = len(tokens)
        for token in tokens:
            if token.pos in [WordMarkers.NON_WORD.name, WordMarkers.NO_POS.name]:
                self.total_non_words += 1

    @property
    def non_word_ratio(self):
        return round(self.total_non_words / self.total_tokens, 2)

    def __add__(self, other):
        return NonWordsCounter(
            total_tokens=self.total_tokens + other.total_tokens,
            total_non_words=self.total_non_words + other.total_non_words,
        )

    def dict(self) -> Dict:
        return {
            "total_tokens": self.total_tokens,
            "total_non_words": self.total_non_words,
            "non_words_ratio": self.non_word_ratio,
        }
