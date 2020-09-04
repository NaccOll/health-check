import base64
import hashlib
import hmac
import time
from json import dumps
from urllib.parse import quote_plus

import requests

from ....logger_factory import Logger
from ..common.abstract_notify import AbstractNotify
from .dingding_robot_properties import DingdingProperties

logger = Logger("dingding-robot", __file__)


def sign_content(timestamp, secret):
    secret_enc = bytes(secret, encoding='utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign, encoding='utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    return quote_plus(base64.b64encode(hmac_code))


class DingdingRobotNotify(AbstractNotify):
    def __init__(self):
        super().__init__()
        self._senders = DingdingProperties()

    def send_text(self, sender_name, text):
        request = {
            'msgtype': 'text',
            'text': {
                'content': text
            },
            'at': ''
        }
        if not sender_name in self._senders.get_all_robot_names():
            return
        sender = self._senders.get_config(sender_name)
        webhook = sender.webhook
        secret = sender.secret
        self._send_request(dumps(request), webhook, secret)

    def _send_request(self, body, webhook, secret):
        timestamp = round(time.time() * 1000)
        sign = sign_content(timestamp, secret)
        webhook = webhook.format(timestamp, sign)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(webhook, data=bytes(
            body, encoding='utf-8'), headers=headers)
        logger.debug(response.json())
