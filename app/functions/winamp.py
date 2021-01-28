"""Winamp module."""

import emoji


class Base:
    """Defining base class for inheritence."""

    def winamp(self):
        """Return random Emoij."""
        thumb = emoji.emojize(':llama:')
        return "It really whips the " + thumb + " ass."
