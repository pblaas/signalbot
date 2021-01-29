import unittest

from signalbot.message import Message


class MessageTest(unittest.TestCase):

    def setUp(self) -> None:
        self.message = Message("+316", "testmessage", "groupid4", 112233)

    def tearDown(self) -> None:
        pass

    def test_lookup_message(self):
        m = self.message.getmessage()
        self.assertEqual("testmessage", m)

    def test_lookup_timestamp(self):
        t = self.message.gettimestamp()
        self.assertEqual("112233", t)

    def test_lookup_source(self):
        s = self.message.getsource()
        self.assertEqual("+316", s)

    def test_lookup_groupinfo(self):
        g = self.message.getgroupinfo()
        self.assertEqual("groupid4", g)

