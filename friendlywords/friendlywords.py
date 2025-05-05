import itertools as it
import os
import random
from types import ModuleType
from typing import List, Union


class FriendlyWords(ModuleType):
    __version__ = "1.1.3"
    DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
    WORD_LISTS = {
        "p": {"path": os.path.join(DATA_PATH, "predicates.txt"), "n": 1450, "list": []},
        "o": {"path": os.path.join(DATA_PATH, "objects.txt"), "n": 3062, "list": []},
        "t": {"path": os.path.join(DATA_PATH, "teams.txt"), "n": 130, "list": []},
        "c": {"path": os.path.join(DATA_PATH, "collections.txt"), "n": 70, "list": []},
    }

    @staticmethod
    def _load_word(txt_file: str, n: int = -1) -> Union[str, List[str]]:
        """Load N-th word from the text file.

        Args:
            txt_file: path to the text file
            n: word number to read and return, if negative, return the whole list

        Returns:
            Single word or list of words

        Raises:
            RuntimeError: If the text file does not exist

        """
        if not os.path.exists(txt_file):
            raise RuntimeError(f"The text file ({txt_file}) does not exist.")

        if n < 0:
            with open(txt_file) as f:
                return [w.rstrip() for w in f]

        with open(txt_file) as f:
            return next(it.islice(f, n, n + 1), None).rstrip()

    @property
    def predicates(self) -> List[str]:
        """Get list of all predicate words."""
        if not self.WORD_LISTS["p"]["list"]:
            self.WORD_LISTS["p"]["list"] = self._load_word(self.WORD_LISTS["p"]["path"], -1)

        return self.WORD_LISTS["p"]["list"]

    @property
    def objects(self) -> List[str]:
        """Get list of all predicate words."""
        if not self.WORD_LISTS["o"]["list"]:
            self.WORD_LISTS["o"]["list"] = self._load_word(self.WORD_LISTS["o"]["path"], -1)

        return self.WORD_LISTS["o"]["list"]

    @property
    def teams(self) -> List[str]:
        """Get list of all team words."""
        if not self.WORD_LISTS["t"]["list"]:
            self.WORD_LISTS["t"]["list"] = self._load_word(self.WORD_LISTS["t"]["path"], -1)

        return self.WORD_LISTS["t"]["list"]

    @property
    def collections(self) -> List[str]:
        """Get list of collection words."""
        if not self.WORD_LISTS["c"]["list"]:
            self.WORD_LISTS["c"]["list"] = self._load_word(self.WORD_LISTS["c"]["path"], -1)

        return self.WORD_LISTS["c"]["list"]

    def preload(self) -> None:
        """Preload all word lists into memory."""
        for w in self.WORD_LISTS:
            self.WORD_LISTS[w]["list"] = self._load_word(self.WORD_LISTS[w]["path"], -1)

    def generate(
        self,
        command: Union[int, str],
        separator: str = " ",
        as_list: bool = False,
    ) -> Union[str, List[str]]:
        """Generate friendly words based on the provided command.
        The command can be an integer (number of words to generate) or a string pattern for specific word types.
        If an integer is provided, it will generate that many words, with the last word being an object.
        The string pattern can contain:
        - 'p' for predicates
        - 'o' for objects
        - 't' for teams
        - 'c' for collections
        The generated words will be joined by the specified separator.
        If `as_list` is True, a list of words will be returned instead of a string, ignoring the separator.

        Args:
            command: Integer (number of words) or string pattern
            separator: String to join words with
            as_list: Whether to return a list of words instead of a string

        Returns:
            String of words joined by separator or a list of words

        Raises:
            TypeError: If command is not int or str, or separator is not str
            ValueError: If command is invalid

        """
        if not isinstance(command, (int, str)):
            raise TypeError(f"Generate expects a positive integer or str, not {type(command)}")

        if not isinstance(separator, str):
            raise TypeError(f"Separator must be a string, not {type(separator)}")

        # define type of words to sample
        if isinstance(command, int):
            if command <= 0:
                raise ValueError("Generate expects a positive integer or str")

            # N-1 predicates + 1 object
            _command = "p" * (command - 1) + "o"
        else:
            _command = command.lower()

        # sample the words according to _command
        words = []
        for c in _command:
            if c not in self.WORD_LISTS:
                raise ValueError("Generate expects chars p (predicate), o (object), t (teams) or c (collections).")

            chosen_word = random.randint(0, self.WORD_LISTS[c]["n"] - 1)

            if self.WORD_LISTS[c]["list"]:
                words.append(self.WORD_LISTS[c]["list"][chosen_word])
            else:
                words.append(self._load_word(self.WORD_LISTS[c]["path"], chosen_word))

        # return as list if needed, otherwise join with separator and return
        if as_list:
            return words
        return separator.join(words)
