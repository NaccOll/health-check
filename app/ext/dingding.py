import time
import hmac
import hashlib
import base64
import requests
from urllib.parse import quote_plus
from json import dumps
from .dingding_properties import DingdingProperties
from framework import Logger
logger = Logger('dingding',__file__)
SECRET = DingdingProperties().secret
WEBHOOK_TEMPLATE = DingdingProperties().webhook_template

REPORTER_MARKDOWN_TEMPLATE = '#### {} \n ![reporter]({}) \n'


def sign_content(timestamp, secret):
    secret_enc = bytes(secret, encoding='utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = bytes(string_to_sign, encoding='utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc,
                         digestmod=hashlib.sha256).digest()
    return quote_plus(base64.b64encode(hmac_code))


def send_request(body, webhook, secret):
    timestamp = round(time.time() * 1000)
    sign = sign_content(timestamp, secret)
    webhook = webhook.format(timestamp, sign)
    headers = {'Content-Type': 'application/json'}
    response = requests.post(webhook, data=bytes(
        body, encoding='utf-8'), headers=headers)
    logger.debug(response.json())


def assembly_markdown(title, image_url):
    return REPORTER_MARKDOWN_TEMPLATE.format(title, image_url)


def assembly_request_json(title, image_url):
    markdown_content = assembly_markdown(title, image_url)
    markdown = Markdown(title, markdown_content)
    request = {'msgtype': 'markdown', 'markdown': markdown.__dict__, 'at': ''}
    return dumps(request, ensure_ascii=False).replace(r'\\n', r'\n')


def send_msg_markdown(title, image_url):
    send_request(assembly_request_json(
        title, image_url), WEBHOOK_TEMPLATE, SECRET)


def send_msg_text(content: str):
    request = {
        'msgtype': 'text',
        'text': {
            'content': content
        },
        'at': ''
    }
    send_request(dumps(request), WEBHOOK_TEMPLATE, SECRET)


class Text:
    def __init__(self, content: str):
        self.content = content


class Markdown:
    def __init__(self,
                 title: str,
                 text: str):
        self.title = title
        self.text = text


if __name__ == "__main__":
    send_msg_text('测试告警')
