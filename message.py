""" Model for Messages """

class Message:

    def __init__(self,source,message,groupinfo,author,version):
        self._source = source
        self._message = message
        self._groupinfo = groupinfo
        self._author = author
        self._version = version

    def getGroupinfo(self):
        return self._groupinfo

    def getMessage(self):
        return self._message

    def getSource(self):
        return self._source

    def getVersion(self):
        return "SignalCLI bot version: " + self._version + " by " + self._author


