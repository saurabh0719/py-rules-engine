from .__version__ import __version__
from .errors import InvalidRuleError


def validate_version(version):
    """
    Validate a rule version.
    """
    if version != __version__:
        raise InvalidRuleError('Invalid version')
