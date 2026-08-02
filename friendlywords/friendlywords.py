import os
import random
import warnings
from types import ModuleType
from typing import Dict, List, Optional, TypedDict, Union


class _WordList(TypedDict):
    path: str
    n: int
    list: List[str]


def _load_words(txt_file: str) -> List[str]:
    """Load all words from the text file.

    Args:
        txt_file: path to the text file

    Returns:
        List of words

    Raises:
        RuntimeError: If the text file does not exist

    """
    if not os.path.exists(txt_file):
        raise RuntimeError(f"The text file ({txt_file}) does not exist.")

    with open(txt_file) as f:
        return [w.rstrip() for w in f]


def _word_list(path: str) -> _WordList:
    words = _load_words(path)
    return {"path": path, "n": len(words), "list": words}


class FriendlyWords(ModuleType):
    __version__: str

    DATA_PATH = os.path.join(os.path.dirname(__file__), "data")
    WORD_LISTS: Dict[str, _WordList] = {
        "p": _word_list(os.path.join(DATA_PATH, "predicates.txt")),
        "o": _word_list(os.path.join(DATA_PATH, "objects.txt")),
        "t": _word_list(os.path.join(DATA_PATH, "teams.txt")),
        "c": _word_list(os.path.join(DATA_PATH, "collections.txt")),
    }

    @property
    def predicates(self) -> List[str]:
        """Get list of all predicate words."""
        return self.WORD_LISTS["p"]["list"]

    @property
    def objects(self) -> List[str]:
        """Get list of all object words."""
        return self.WORD_LISTS["o"]["list"]

    @property
    def teams(self) -> List[str]:
        """Get list of all team words."""
        return self.WORD_LISTS["t"]["list"]

    @property
    def collections(self) -> List[str]:
        """Get list of collection words."""
        return self.WORD_LISTS["c"]["list"]

    def preload(self) -> None:
        """Deprecated: word lists are always loaded at import, this method is a no-op."""
        warnings.warn(
            "preload() is deprecated and no longer needed: word lists are always loaded at import.",
            DeprecationWarning,
            stacklevel=2,
        )

    def generate(
        self,
        command: Union[int, str],
        separator: str = " ",
        as_list: bool = False,
        rng: Optional[random.Random] = None,
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
        If `rng` is provided, it is used as the source of randomness instead of the global `random` state,
        making generation reproducible without touching the global seed.

        Args:
            command: Integer (number of words) or string pattern
            separator: String to join words with
            as_list: Whether to return a list of words instead of a string
            rng: Optional `random.Random` instance to use as the source of randomness

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
            if not command:
                raise ValueError("Generate expects a non-empty str")

            _command = command.lower()

        randint = rng.randint if rng is not None else random.randint

        # sample the words according to _command
        words: List[str] = []
        for c in _command:
            if c not in self.WORD_LISTS:
                raise ValueError("Generate expects chars p (predicate), o (object), t (teams) or c (collections).")

            word_list = self.WORD_LISTS[c]["list"]
            words.append(word_list[randint(0, len(word_list) - 1)])

        # return as list if needed, otherwise join with separator and return
        if as_list:
            return words
        return separator.join(words)
