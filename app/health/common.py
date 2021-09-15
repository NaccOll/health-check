import requests
from .abstract_health import AbstractHealth, HealthError
from requests.packages.urllib3.exceptions import ReadTimeoutError
from ..properties.health_properties import HealthItem, HttpParam


class CommonHttpHealth(AbstractHealth):
    def __init__(self, config: HealthItem):
        if config.type != 'http':
            raise TypeError("the type of config require is http")
        super().__init__(config)
        self.http_param: HttpParam = config.http_param

    def _do_health(self):
        config = self.config
        if len(config.imports) > 0:
            for import_cls in config.imports:
                exec("global {import_cls};import {import_cls};".format(
                    import_cls=import_cls))
        res = None
        param: HttpParam = self.http_param
        url = ''
        headers = {}
        if not param.url_param is None:
            url_param = {key: eval(value)
                         for key, value in param.url_param.items()}
            url = param.http_url.format(**url_param)
        if not param.headers is None:
            headers = {key: value
                       for key, value in param.headers.items()}
        try:
            if param.http_method.upper() == "GET":
                res = requests.get(
                    url, headers=headers, timeout=config.timeout+1)
            if param.http_method.upper() == "POST":
                pass
            if param.http_method.upper() == "PUT":
                pass
        except ReadTimeoutError as e:
            raise HealthError("请求超时")
        if res is None:
            raise HealthError("响应结果为空")
        if res.status_code >= 400:
            raise HealthError("请求有误,响应状态码: {status} 原因: {reason}".format(
                status=res.status_code, reason=res.reason))
        
        text = res.text if res.encoding == 'utf-8' else res.text.encode(res.encoding).decode('utf-8')
        if param.match_type and param.match_content not in text:
            raise HealthError("响应结果匹配错误, 响应结果文本: "+text)
        if not param.match_type and param.match_content in text:
            raise HealthError("响应结果不应匹配")
