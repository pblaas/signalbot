""" Model for Messages """

class Message:

    def __init__(self,source,message,groupinfo):
        self._source = source
        self._message = message
        self._groupinfo = groupinfo

    def getGroupinfo(self):
        return self._groupinfo

    def getMessage(self):
        return self._message

    def getSource(self):
        return self._source


