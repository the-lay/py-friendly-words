import os
import random
import itertools as it
from types import ModuleType
from typing import List, Union


class FriendlyWords(ModuleType):

    __version__ = '1.0.2'
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
    WORD_LISTS = {
        'p': {
            'path': os.path.join(DATA_PATH, 'predicates.txt'),
            'n': 1455,
            'list': []
        },
        'o': {
            'path': os.path.join(DATA_PATH, 'objects.txt'),
            'n': 3073,
            'list': []
        },
        't': {
            'path': os.path.join(DATA_PATH, 'teams.txt'),
            'n': 130,
            'list': []
        },
        'c': {
            'path': os.path.join(DATA_PATH, 'collections.txt'),
            'n': 70,
            'list': []
        }
    }

    @staticmethod
    def _load_word(txt_file: str, n: int = -1):
        """
        Loads N-th word from the text file

        :param txt_file: str, path to the text file
        :param n: int, word number to read and return, if negative, return the whole list
        :return: word or list of words
        """
        if not os.path.exists(txt_file):
            raise RuntimeError(f'The text file ({txt_file}) does not exist.')

        if n < 0:
            return [w.rstrip() for w in open(txt_file, mode='r')]

        with open(txt_file, mode='r') as f:
            return next(it.islice(f, n, n+1), None).rstrip()

    @property
    def predicates(self) -> List[str]:
        if not self.WORD_LISTS['p']['list']:
            self.WORD_LISTS['p']['list'] = self._load_word(self.WORD_LISTS['p']['path'], -1)

        return self.WORD_LISTS['p']['list']

    @property
    def objects(self) -> List[str]:
        if not self.WORD_LISTS['o']['list']:
            self.WORD_LISTS['o']['list'] = self._load_word(self.WORD_LISTS['o']['path'], -1)

        return self.WORD_LISTS['o']['list']

    @property
    def teams(self) -> List[str]:
        if not self.WORD_LISTS['t']['list']:
            self.WORD_LISTS['t']['list'] = self._load_word(self.WORD_LISTS['t']['path'], -1)

        return self.WORD_LISTS['t']['list']

    @property
    def collections(self) -> List[str]:
        if not self.WORD_LISTS['c']['list']:
            self.WORD_LISTS['c']['list'] = self._load_word(self.WORD_LISTS['c']['path'], -1)

        return self.WORD_LISTS['c']['list']

    def preload(self):
        for w in self.WORD_LISTS:
            self.WORD_LISTS[w]['list'] = self._load_word(self.WORD_LISTS[w]['path'], -1)

    def generate(self, command: Union[int, str], separator: str = ' ', as_list: bool = False):

        if not isinstance(command, int) and not isinstance(command, str):
            raise TypeError(f'Generate expects a positive integer or str, not {type(command)}')

        # define type of words to sample
        if isinstance(command, int):
            if command < 0:
                raise ValueError('Generate expects a positive integer or str')

            # N-1 predicates + 1 object
            _command = 'o'
            for i in range(command - 1):
                _command = 'p' + _command
        else:
            _command = command.lower()

        # sample the words according to _command
        words = []
        for c in _command:
            if c not in self.WORD_LISTS:
                raise ValueError('Generate expects chars p (predicate), o (object), t (teams) or c (collections).')

            chosen_word = random.randrange(0, self.WORD_LISTS[c]['n'])

            if self.WORD_LISTS[c]['list']:
                words.append(self.WORD_LISTS[c]['list'][chosen_word])
            else:
                words.append(self._load_word(self.WORD_LISTS[c]['path'], chosen_word))

        # return as list if needed, otherwise join with separator and return
        if as_list:
            return words
        else:
            return separator.join(words)
