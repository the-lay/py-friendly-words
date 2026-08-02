import random
from typing import Dict, List, Literal, Optional, TypedDict, Union, overload

__version__: str

class _WordList(TypedDict):
    path: str
    n: int
    list: List[str]

WORD_LISTS: Dict[str, _WordList]
predicates: List[str]
objects: List[str]
teams: List[str]
collections: List[str]

def preload() -> None: ...
@overload
def generate(
    command: Union[int, str],
    separator: str = ...,
    as_list: Literal[False] = ...,
    rng: Optional[random.Random] = ...,
) -> str: ...
@overload
def generate(
    command: Union[int, str],
    separator: str,
    as_list: Literal[True],
    rng: Optional[random.Random] = ...,
) -> List[str]: ...
@overload
def generate(
    command: Union[int, str],
    separator: str = ...,
    *,
    as_list: Literal[True],
    rng: Optional[random.Random] = ...,
) -> List[str]: ...
