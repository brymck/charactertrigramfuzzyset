########################
charactertrigramfuzzyset
########################

Character trigram fuzzy set implementation providing cosine similarity-based
fuzzy matching.

This library does that one thing on iterables of strings. Any beyond
that--Levenshtein distance, scoring, bigram fallback, etc.--is left as an
exercise to the reader.

*****
Usage
*****

.. code-block:: python

    import os.path
    from timeit import timeit
    import requests

    # Retrieve a file containing around 470,000 English words
    url = 'https://github.com/dwyl/english-words/raw/master/words.txt'
    r = requests.get(url, stream=True)
    words_path = os.path.expanduser('~/words.txt')
    if not os.path.isfile(words_path):
        with open(words_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    # Usage
    import charactertrigramfuzzyset as ctfs
    items = [line.rstrip() for line in open(words_path, 'r')]
    fs = ctfs.CharacterTrigramFuzzySet(items)
    fs.get('bryan')

    # Profiling, generally around 10-20 ms per call on my machine
    timeit("fs.get('bryan')", setup='''
    import charactertrigramfuzzyset as ctfs
    items = [line.rstrip() for line in open('{words_path}', 'r')]
    fs = ctfs.CharacterTrigramFuzzySet(items)
    '''.format(words_path=words_path), number=1000)
