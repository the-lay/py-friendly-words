import sys
from .friendlywords import FriendlyWords

__version__ = FriendlyWords.__version__
sys.modules[__name__] = FriendlyWords(__name__)
