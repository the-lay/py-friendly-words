import sys
from .friendlywords import FriendlyWords

sys.modules[__name__] = FriendlyWords(__name__)
