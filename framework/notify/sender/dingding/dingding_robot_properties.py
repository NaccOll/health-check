from typing import Dict

from ....struct.config_properties import ConfigProperties
from ....enable_configuation import enable_configuation


class DingDingItem:
    webhook = ''
    secret = ''

    def __init__(self, webhook, secret):
        super().__init__()
        self.webhook = webhook
        self.secret = secret


@enable_configuation(prefix='notify.dingding-robot')
class DingdingProperties(ConfigProperties):
    _robots: Dict[str, DingDingItem] = {}

    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config: Dict):
        if config is None or len(config.keys()) == 0:
            return
        for robot_name, config_value in config.items():
            if robot_name in self._robots:
                raise AttributeError("dingding robot name dulpduplicate")
            self._robots[robot_name] = DingDingItem(
                config_value.webhook,
                config_value.secret
            )

    def get_all_robot_names(self):
        return self._robots.keys()

    def get_config(self, key):
        return self._robots.get(key, None)
