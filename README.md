# py-friendly-words
BADGES GO HERE

Python package to generate random human-readable strings. The word lists are taken from
[glitchdomcom/friendly-words](https://github.com/glitchdotcom/friendly-words) and the package provides
a convenient way to access it, as well as methods to easily generate combinations.

The package is fairly simple and somewhat limited.
If you need an extensive customization, uniqueness guarantees, bigger and/or custom dictionaries, check out
[alexanderlukanin13/coolname](https://github.com/alexanderlukanin13/coolname).

Features
--------
- No extra dependencies
- Optional preloading to avoid re-reading word list files
- Customizable generation (see the guide below)

Quick guide
-----------
```python
import friendlywords as fw

# optional preloading, load all word lists into memory (~TODO measure MB)
# otherwise every generation would involve reading the files
fw.preload()

# generate random string that consists of N words (N > 0)
# if N is 1, the returned word is an object
# if N > 1, the first N-1 words are predicates
fw.generate(1)
>>> 'guardian'
fw.generate(4)
>>> 'iridescent angry bald guardian'

# generate string that consists of a random predicate and random object
# p = predicate, o = object, t = team, c = collection
fw.generate('po')
>>> 'shrouded guardian'
fw.generate('PT')
>>> 'SHROUDED ALLIANCE'
fw.generate('Co')
>>> 'Compilation turnip'

# specify the separator
fw.generate('po', separator='-')
>>> 'shrouded-guardian'
fw.generate('ppp', separator=', ')
>>> 'iridescent, angry, bald'
fw.generate(3, separator='/')
>>> 'shrouded/bald/guardian' 

# return list of words instead of a string (ignores separator keyword)
fw.generate(2, list=True)
>>> ['shrouded', 'guardian']
fw.generate('po', list=True)
>>> ['shrouded', 'guardian']

# lists of all predicates, objects, teams or collections
fw.predicates, fw.objects, fw.teams, fw.collections
>>> ['windy', ...], ['turnip', ...], ['alliance', ...], ['album', ...]
```
