from typing import List, Dict
from framework import enable_configuation
from framework.struct.config_properties import ConfigProperties


class HttpParam:
    def __init__(self, config):
        self.http_url: str = config['http-url']
        self.body: str = config['body'] if 'body' in config else None
        self.body_param: Dict[str, str] = {name: value for (name, value) in config['body-param'].items()} \
            if 'body-param' in config else None
        self.url_param: Dict[str, str] = {name: value for (name, value) in config['url-param'].items()} \
            if 'url-param' in config else None
        self.headers: Dict[str, str] = {name: value for (name, value) in config['headers'].items()} \
            if 'headers' in config else None
        self.http_method: str = config['http-method']
        self.match_type: bool = config['match-type']
        self.match_content: str = config['match-content']
        self.extra_check: str = config['extra-check'] if 'extra-check' in config else None
        self.ignore_status_error: str = config['ignore-status-error'] if 'ignore-status-error' in config else False


class HealthItem:
    def __init__(self, config):
        self.name: str = config['name']
        self.exec: str = config['exec']
        self.exec_class: str = config['exec-class']
        self.frequency: int = config['frequency']
        self.fail_notify_count: int = config['fail-notify-count']
        self.timeout_rel: str = config['timeout-rel']
        self.timeout: str = config['timeout']
        self.ignore_timeout_error: bool = config['ignore-timeout-error'] if 'ignore-timeout-error' in config else False 
        self.imports: List[str] = config['imports'] if "imports" in config else []
        self.fail_silent_period: int = config['fail-silent-period'] if "fail-silent-period" in config else 1800
        self.start_time = config['start_time'] if "start_time" in config else '00:00:00'
        self.end_time = config['end_time'] if "end_time" in config else '23:59:59'
        self.receivers = config.get('receivers', [])
        self.type: str = config['type']
        self.http_param: HttpParam = HttpParam(config['http-param'])


@enable_configuation(prefix='health')
class HealthProperties(ConfigProperties):
    configs: List[HealthItem] = []

    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config):
        self.configs = [HealthItem(i) for i in config.configs]
