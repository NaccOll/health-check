import unittest
from framework import Config


class TestDingDingRobot(unittest.TestCase):
    def setUp(self):
        Config.load_config()

    def test_send(self):
        from framework.notify.sender.dingding.dingding_robot import DingdingRobotNotify
        DingdingRobotNotify().send_text('dyt-error-notify', '测试')
