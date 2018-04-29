# Much of this code is inspired by or straight from the original `fuzzyset` for
# Python, which you can find here:
#   https://github.com/axiak/fuzzyset
#
# That library hasn't been updated much and has some inefficiencies that I
# wanted to address in a pure Python implementation

import re
from math import sqrt
from operator import itemgetter
from collections import defaultdict

_non_word_sub = re.compile(r'[^\w, ]+').sub
__version__ = '0.0.1'


class CharacterTrigramFuzzySet(object):
    def __init__(self, iterable, max_count=100, relative_threshold=0.5):
        self._match_dict = defaultdict(list)
        self._items = []
        for value in iterable:
            self._add(value)
        self.max_count = max_count
        self.relative_threshold = relative_threshold

    def _add(self, value):
        lvalue = value.lower()
        simplified = '-' + _non_word_sub('', lvalue) + '-'
        gram_count = len(simplified) - 2
        idx = len(self._items)
        for i in range(gram_count):
            self._match_dict[simplified[i:i + 3]].append(idx)
        self._items.append((sqrt(gram_count), lvalue))

    def get(self, value):
        simplified = '-' + _non_word_sub('', value.lower()) + '-'
        gram_count = len(simplified) - 2
        norm = sqrt(gram_count)

        matches = defaultdict(float)
        match_dict = self._match_dict
        for i in range(gram_count):
            for idx in match_dict[simplified[i:i + 3]]:
                matches[idx] += 1

        items = self._items
        results = [(match_score / (norm * items[idx][0]), items[idx][1])
                   for idx, match_score in matches.items()]
        results.sort(reverse=True, key=itemgetter(0))

        threshold = results[0][0] * self.relative_threshold
        return [(score, lval)
                for score, lval in results[:self.max_count]
                if score > threshold]
