"""Rand module."""

from haikunator import Haikunator


class Rand:
    """Defining base class for inheritence."""

    @staticmethod
    def rand():
        """Return a random number between 0 and 1000."""
        haikunator = Haikunator()
        return haikunator.haikunate(token_length=0, delimiter=' ')
