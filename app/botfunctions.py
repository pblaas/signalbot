"""Collection of Bot functions."""

from functions import help, test, version, gif, chuck, flip, rand, haiku, me, bored, trivia, gnews, twitch, hn, dog, winamp


class SwitchCase(
    help.Base, test.Base, version.Base, gif.Base, chuck.Base, flip.Base, rand.Base,
    haiku.Base, me.Base, bored.Base, hn.Base, dog.Base, winamp.Base,
    trivia.Base, gnews.Base, twitch.Base
):
    """SwitchCase class to switch bot functions."""

    def __init__(self, version, author, signalexecutorlocal, messageobject):
        """Initialize SwitchCase with version, author, signalexecutor and the messagestring."""
        self._version = version
        self._author = author
        self._signalexecutorlocal = signalexecutorlocal
        self._messageobject = messageobject

    def switch(self, action):
        """Switch function to switch between available functions."""
        default = "Invalid option."
        return getattr(self, str(action)[1:].split()[0], lambda: default)()
