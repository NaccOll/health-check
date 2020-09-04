from typing import Dict

from ....enable_configuation import enable_configuation
from ....struct.config_properties import ConfigProperties


class EnterpriseWechatRobotItem:
    webhook = ''

    def __init__(self, webhook):
        super().__init__()
        self.webhook = webhook


@enable_configuation(prefix='notify.enterprise-wechat-robot')
class EnterpriseWechatRobotProperties(ConfigProperties):
    _robots: Dict[str, EnterpriseWechatRobotItem] = {}

    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config: Dict):
        if config is None or len(config.keys()) == 0:
            return
        for robot_name, config_value in config.items():
            if robot_name in self._robots:
                raise AttributeError(
                    "enterprise wechat robot name dulpduplicate")
            self._robots[robot_name] = EnterpriseWechatRobotItem(
                config_value.webhook
            )

    def get_all_robot_names(self):
        return self._robots.keys()

    def get_config(self, key):
        return self._robots.get(key, None)
