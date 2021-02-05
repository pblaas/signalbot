"""Winamp module."""

import emoji


class Winamp:
    """Defining base class for inheritence."""

    @staticmethod
    def winamp():
        """Return random Emoij."""
        thumb = emoji.emojize(':llama:')
        return "It really whips the " + thumb + " ass."
