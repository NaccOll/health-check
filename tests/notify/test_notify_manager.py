import unittest
from framework import Config


class TestNotifyManager(unittest.TestCase):
    def setUp(self):
        Config.load_config()

    def test_send(self):
        from framework.notify import NotifyManager
        NotifyManager().send_groups_text(['dyt-it'], '测试')
