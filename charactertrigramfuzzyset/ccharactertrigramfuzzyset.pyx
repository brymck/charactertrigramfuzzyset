from operator import itemgetter
from libc.math cimport sqrt

cdef class CharacterTrigramFuzzySet:
    cdef dict _match_dict
    cdef list _items
    cdef set _seen
    cdef int _max_count
    cdef float _relative_threshold
    
    def __cinit__(self, iterable, int max_count=100, float relative_threshold=0.5):
        self._match_dict = {}
        self._items = []
        self._seen = set()
        cdef str value
        for value in iterable:
            self._add(value)
        self._max_count = max_count
        self._relative_threshold = relative_threshold

    cdef _add(self, str value):
        cdef str lvalue = value.lower()
        cdef str simplified = '-' + lvalue + '-'
        if lvalue in self._seen:
            return
        self._seen.update(lvalue)
        cdef int gram_count = len(simplified) - 2
        cdef int idx = len(self._items)
        cdef int i
        cdef str gram
        for i in range(gram_count):
            gram = simplified[i:i + 3]
            if gram in self._match_dict:
                self._match_dict[gram].append(idx)
            else:
                self._match_dict[gram] = [idx]
        self._items.append(tuple([sqrt(gram_count), lvalue]))

    cpdef list get(self, str value):
        cdef str simplified = '-' + value.lower() + '-'
        cdef int gram_count = len(simplified) - 2
        cdef float norm = sqrt(gram_count)

        cdef dict matches = {}
        cdef dict match_dict = self._match_dict
        cdef int i
        cdef int idx
        for i in range(gram_count):
            for idx in match_dict.get(simplified[i:i + 3], ()):
                if idx in matches:
                    matches[idx] += 1
                else:
                    matches[idx] = 1

        cdef list items = self._items
        cdef list results = [(match_score / (norm * items[idx][0]), items[idx][1])
                   for idx, match_score in matches.items()]
            
        if not results:
            return results
        results.sort(reverse=True, key=itemgetter(0))

        cdef float threshold = results[0][0] * self._relative_threshold
        cdef float score
        cdef str lval
        return [tuple([score, lval])
                for score, lval in results[:self._max_count]
                if score > threshold]