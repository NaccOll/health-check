from json import dumps

import requests

from ..common.abstract_notify import AbstractNotify
from .enterprise_wechat_robot_properties import EnterpriseWechatRobotProperties


class EnterpriseWechatRobotNotify(AbstractNotify):
    def __init__(self):
        super().__init__()
        self._senders = EnterpriseWechatRobotProperties()

    def send_text(self, sender_name, content: str):
        request = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        if not sender_name in self._senders.get_all_robot_names():
            return
        sender = self._senders.get_config(sender_name)
        webhook = sender.webhook
        self._send_request(dumps(request), webhook)

    def _send_request(self, body, webhook):
        headers = {'Content-Type': 'application/json'}
        res = requests.post(webhook, data=bytes(
            body, encoding='utf-8'), headers=headers)
        print(res)
