from ..metaclass.singleton_meta import SingletonMeta
from .receive.receive_properties import ReceiveProperties
from .sender import (DingdingRobotNotify, EnterpriseWechatAppNotify,
                     EnterpriseWechatRobotNotify)


class NotifyManager(metaclass=SingletonMeta):
    def __init__(self):
        super().__init__()
        self._receivers = ReceiveProperties()
        self._dingding_notify = DingdingRobotNotify()
        self._enterprise_wechat_app_notify = EnterpriseWechatAppNotify()
        self._enterprise_wechat_robot_notify = EnterpriseWechatRobotNotify()

    def send_group_text(self, group_name, text):
        self.send_groups_text([group_name], text)

    def send_groups_text(self, group_names, text):
        usernames = self._receivers.get_usernames_by_groupnames(group_names)
        self.send_users_text(usernames, text)

    def send_users_text(self, usernames, text):
        users = self._receivers.get_user_configs_by_usernames(usernames)
        dingding_robots = set()
        enterprise_wechat_robots = set()
        enterprise_wechat_apps = set()
        for u in users:
            if u.dingding_robot is not None:
                dingding_robots.add(u.dingding_robot)
            if u.enterprise_wechat_robot is not None:
                enterprise_wechat_robots.add(u.enterprise_wechat_robot)
            if u.enterprise_wechat_app is not None:
                enterprise_wechat_apps.add(u.enterprise_wechat_app)
        for sender_name in dingding_robots:
            self._dingding_notify.send_text(sender_name, text)
        for sender_name in enterprise_wechat_robots:
            self._enterprise_wechat_robot_notify.send_text(sender_name, text)
        for sender_name in enterprise_wechat_apps:
            self._enterprise_wechat_app_notify.send_text(sender_name, text)

    def send_user_text(self, username, text):
        self.send_users_text([username], text)
