import unittest
from framework import Config


class TestEnterpriseWechatApp(unittest.TestCase):
    def setUp(self):
        Config.load_config()

    def test_send(self):
        # print('hello')
        from framework.notify.sender.enterprise_wechat_app.enterprise_wechat_app import EnterpriseWechatAppNotify
        EnterpriseWechatAppNotify().send_text('dyt-error-notify', '测试')
