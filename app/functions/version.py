"""Version module."""


class Version:
    """Defining base class for inheritence."""

    def version(self):
        """Return version information."""
        return "SignalCLI bot version: " + self._version + " by " + self._author
