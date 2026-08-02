import importlib.metadata
import sys

from .friendlywords import FriendlyWords

_module = FriendlyWords(__name__)
try:
    _module.__version__ = importlib.metadata.version("friendlywords")
except importlib.metadata.PackageNotFoundError:
    _module.__version__ = "0+unknown"
sys.modules[__name__] = _module
