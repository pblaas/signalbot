"""Me module."""

import emoji


class Me:
    """Defining base class for inheritence."""

    @staticmethod
    def me():
        """Return eggplant Emoij."""
        thumb = emoji.emojize(':eggplant:')
        return thumb
