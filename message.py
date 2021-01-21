"""Message module."""


class Message:
    """Message class to model data."""

    def __init__(self, source, message, groupinfo):
        """Initialize Message object with source, message and groupinfo."""
        self._source = source
        self._message = message
        self._groupinfo = groupinfo

    def getgroupinfo(self):
        """Return groupID."""
        return self._groupinfo

    def getmessage(self):
        """Return message string."""
        return self._message

    def getsource(self):
        """Return initiator of the message."""
        return self._source
