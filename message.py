""" Message module """


class Message:
    """ Message class to model data """
    def __init__(self, source, message, groupinfo):
        self._source = source
        self._message = message
        self._groupinfo = groupinfo

    def getgroupinfo(self):
        """ return groupID """
        return self._groupinfo

    def getmessage(self):
        """ return message string """
        return self._message

    def getsource(self):
        """ return initiator of the message """
        return self._source
