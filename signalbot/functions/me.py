"""Me module."""

import emoji


class Me:
    """Defining base class for inheritence."""

    @staticmethod
    def me():
        """Return random Emoij."""
        thumb = emoji.emojize(':eggplant:')
        return thumb
