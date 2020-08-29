from framework.struct.config_properties import ConfigProperties
from framework.enable_configuation import enable_configuation


@enable_configuation(prefix='notify.dingding')
class DingdingProperties(ConfigProperties):
    secret = ''
    webhook_template = ''
    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config):
        self.secret = config.secret
        self.webhook_template = config.webhook_template

