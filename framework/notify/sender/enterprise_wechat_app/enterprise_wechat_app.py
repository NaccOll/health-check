from json import dumps, loads

import requests

from ....logger_factory import Logger
from ..common.abstract_notify import AbstractNotify
from .enterprise_wechat_app_properties import EnterpriseWechatAppProperties

logger = Logger('enterprise-wechat-app', __file__)


class EnterpriseWechatAppNotify(AbstractNotify):
    def __init__(self):
        super().__init__()
        self._senders = EnterpriseWechatAppProperties()

    def send_text(self, sender_name, content: str):
        if not sender_name in self._senders.get_all_robot_names():
            return
        sender = self._senders.get_config(sender_name)
        corpid = sender.corpid
        app_id = sender.app_id
        secret = sender.secret
        request = {
            "msgtype": "text",
            "agentid": app_id,
            "text": {
                "content": content
            },
        }
        if sender.toparty is not None:
            request['toparty'] = sender.toparty
        if sender.touser is not None:
            request['touser'] = sender.touser
        self._send_request(dumps(request), corpid, app_id, secret)

    def _send_request(self, body, corpid, app_id, secret):
        token_res = requests.get(
            f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}')
        if not 300 > token_res.status_code >= 200:
            raise RuntimeError(
                f"get enterprise wechat app token fail, corpid={corpid}")
        token_res_data = loads(token_res.content)
        if token_res_data.get('errcode', None) != 0:
            error_reason = token_res_data.errmsg
            raise RuntimeError(
                f"get enterprise wechat app token fail, corpid={corpid}, reason: {error_reason}")
        access_token = token_res_data.get('access_token')
        headers = {'Content-Type': 'application/json'}
        res = requests.post(
            f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}', data=body, headers=headers)
        logger.info(res)
