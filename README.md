# py-friendly-words
[![PyPI version](https://badge.fury.io/py/friendlywords.svg)](https://badge.fury.io/py/friendlywords)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/friendlywords)](https://pypistats.org/packages/friendlywords)
[![Development](https://github.com/the-lay/py-friendly-words/actions/workflows/development.yml/badge.svg)](https://github.com/the-lay/py-friendly-words/actions/workflows/development.yml)

Python package to generate random human-readable strings, e.g. project and experiment names.
The word lists are taken from
[glitchdotcom/friendly-words](https://github.com/glitchdotcom/friendly-words) and the package provides
a convenient way to access it, as well as methods to easily generate combinations.

The package is simple, limited, and over-engineered at the same time.
In other words, a weekend night side project.
If you need a stable package with more extensive customization, uniqueness guarantees,
bigger and/or custom dictionaries, check out
[alexanderlukanin13/coolname](https://github.com/alexanderlukanin13/coolname).

Features
--------
- No extra dependencies
- Word lists are loaded once at import (~41KB in memory)
- Customizable generation (see the examples below)
- Custom separators
- Can return as a list of words
- Reproducible generation with your own `random.Random` instance
- Fully typed public API

Quick guide
-----------
Install with PIP: `pip install friendlywords`

```python
import friendlywords as fw

# generate random string that consists of N words (N > 0)
# if N is 1, the returned word is an object
# if N > 1, the first N-1 words are predicates
fw.generate(1)
>>> 'square'
fw.generate(4)
>>> 'southern florentine rain college'

# generate string that follow a given grammar
# p = predicate, o = object, t = team, c = collection
fw.generate('po')
>>> 'bittersweet curio'
fw.generate('pt')
>>> 'wood organization'
fw.generate('co')
>>> 'selection title'

# specify the separator
fw.generate('po', separator='-')
>>> 'better-tabletop'
fw.generate('ppp', separator=', ')
>>> 'elegant, skitter, sunny'
fw.generate(3, separator='/')
>>> 'winter/alkaline/handsaw' 

# return list of words instead of a string (ignores separator keyword)
fw.generate(5, as_list=True)
>>> ['laced', 'polyester', 'ossified', 'cyclic', 'chronometer']
fw.generate('pppoc', as_list=True)
>>> ['able', 'splendid', 'harvest', 'hedge', 'playlist']

# reproducible generation without touching the global random state
import random
fw.generate('po', rng=random.Random(42))
>>> 'tidal cardboard'

# lists of all predicates, objects, teams or collections
fw.predicates, fw.objects, fw.teams, fw.collections
>>> ['windy', ...], ['turnip', ...], ['alliance', ...], ['album', ...]
```

Notes
-----
- For reproducible output, pass your own `random.Random` instance via the `rng` keyword
  (setting the global `random.seed()` also still works).
- The words are sampled with a non-cryptographic PRNG, so the generated names are readable, not unguessable —
  don't use them as secrets or unique identifiers.
- `fw.preload()` is deprecated and is no longer needed: word lists are always loaded at import.
