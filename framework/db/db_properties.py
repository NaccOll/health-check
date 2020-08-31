from ..struct.config_properties import ConfigProperties
from ..enable_configuation import enable_configuation


@enable_configuation(prefix='datasource')
class DatasourceProperties(ConfigProperties):
    dialect = ''
    driver = ''
    user = ''
    password = ''
    host = ''
    dbname = ''

    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config):
        self.dialect = config.dialect
        self.driver = config.driver
        self.user = config.user
        self.password = config.password
        self.host = config.host
        self.dbname = config.dbname
