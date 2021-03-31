"""Rand module."""

from haikunator import Haikunator


class Rand:
    """Defining base class for inheritence."""

    @staticmethod
    def rand():
        """Return a random string.."""
        haikunator = Haikunator()
        return haikunator.haikunate(token_length=0, delimiter=' ')
