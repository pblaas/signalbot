"""Me module."""

import emoji


class Base:
    """Defining base class for inheritence."""

    def me(self):
        """Return random Emoij."""
        thumb = emoji.emojize(':eggplant:')
        return thumb
