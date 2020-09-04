from typing import Dict, List

from ...enable_configuation import enable_configuation
from ...struct.config_properties import ConfigProperties


class ReceiverItem:
    dingding_robot = None
    enterprise_wechat_robot = None
    enterprise_wechat_app = None

    def __init__(self, dingding_robot,
                 enterprise_wechat_robot,
                 enterprise_wechat_app):
        super().__init__()
        self.dingding_robot = dingding_robot
        self.enterprise_wechat_robot = enterprise_wechat_robot
        self.enterprise_wechat_app = enterprise_wechat_app


@enable_configuation(prefix="receiver")
class ReceiveProperties(ConfigProperties):
    _users: Dict[str, ReceiverItem] = {}
    _groups: Dict[str, List[str]] = {}

    def __init__(self, config=None):
        super().__init__(config=config)

    def load_config(self, config):
        for (key, value) in config.users.items():
            self._users[key] = ReceiverItem(
                value.get('dingding-robot', None),
                value.get('enterprise-wechat-robot', None),
                value.get('enterprise-wechat-app', None)
            )
        self._groups = config.groups

    def get_usernames_by_groupnames(self, group_names: List[str]):
        user_sets = set()
        for group_name in group_names:
            sub_user_in_group = self._groups.get(group_name, [])
            for user_name in sub_user_in_group:
                user_sets.add(user_name)
        return user_sets

    def get_usernames_by_groupname(self, group_name: str):
        return self.get_users_by_groupnames([group_name])

    def get_user_configs_by_usernames(self, usernames):
        result: List[ReceiverItem] = []
        for user_name in usernames:
            user = self._users.get(user_name, None)
            if user is None:
                continue
            result.append(user)
        return result

    def get_user_configs_by_username(self, username):
        return self.get_user_configs_by_usernames([username])
