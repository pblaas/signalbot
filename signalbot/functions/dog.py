"""Dog module."""

import emoji


class Dog:
    """Defining base class for inheritence."""

    @staticmethod
    def dog():
        """Return dog Emoij."""
        dog = emoji.emojize(':dog:')
        return dog + " WOEF,  WAFFF! " + dog
