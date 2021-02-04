"""Test emoji module."""

import emoji


class TestEmoji:
    """Defining base class for inheritence."""

    @staticmethod
    def testemoji():
        """Return random Emoij."""
        tv2 = emoji.emojize(':tv2:')
        movie_camera = emoji.emojize(':movie_camera:')
        apple2 = emoji.emojize(':apple2:')
        lemon = emoji.emojize(':lemon:')
        pineapple = emoji.emojize(':pineapple:')
        pear = emoji.emojize(':pear:')
        tomato = emoji.emojize(':tomato:')

        return tv2 + " " + movie_camera + " " + apple2 + " " + lemon + " " + pineapple + " " + pear + " " + tomato
