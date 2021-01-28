"""Dog module."""

import emoji


class Base:
    """Defining base class for inheritence."""

    def dog(self):
        """Return random Emoij."""
        dog = emoji.emojize(':dog:')
        return dog + " WOEF,  WAFFF! " + dog
