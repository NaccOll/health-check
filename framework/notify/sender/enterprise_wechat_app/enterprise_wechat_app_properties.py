from typing import Dict

from ....enable_configuation import enable_configuation
from ....struct.config_properties import ConfigProperties


class EnterpriseWechatAppItem:
    corpid = ''
    app_id = ''
    secret = ''
    touser = ''
    toparty = ''

    def __init__(self, corpid, app_id, secret, touser='', toparty=''):
        super().__init__()
        self.corpid = corpid
        self.app_id = app_id
        self.secret = secret
        self.touser = touser
        self.toparty = toparty


@enable_configuation(prefix='notify.enterprise-wechat-app')
class EnterpriseWechatAppProperties(ConfigProperties):
    _robots: Dict[str, EnterpriseWechatAppItem] = {}

    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config: Dict):
        if config is None or len(config.keys()) == 0:
            return
        for robot_name, config_value in config.items():
            if robot_name in self._robots:
                raise AttributeError(
                    "enterprise wechat robot name dulpduplicate")
            self._robots[robot_name] = EnterpriseWechatAppItem(
                config_value.get('corpid'),
                config_value.get('app-id'),
                config_value.get('secret'),
                config_value.get('touser', None),
                config_value.get('toparty', None)
            )

    def get_all_robot_names(self):
        return self._robots.keys()

    def get_config(self, key):
        return self._robots.get(key, None)
