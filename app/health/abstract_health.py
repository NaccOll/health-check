import datetime
import time
from abc import abstractmethod

from app.properties.health_properties import HealthItem
from framework import Logger
from framework.notify import NotifyManager


def getTime():
    return int(round(time.time() * 1000))


class HealthError(RuntimeError):

    def __init__(self, message, selected_receiver=None):
        super().__init__(message, None)
        self.selected_receiver = selected_receiver


class AbstractHealth:
    def __init__(self, config: HealthItem):
        self.config = config
        self.last_check_date = None
        self.last_fail_notify_date = None
        self.last_receives = []
        self.fail_count = 0
        self.fail_notify_count = 0
        self.pending = False

        self.logger = Logger(self.config.name, __file__)

    def do_health(self):
        self.load_import()
        config = self.config
        current = getTime()
        start_time = datetime.datetime.strptime(datetime.datetime.now().strftime(
            "%Y-%m-%d")+" "+config.start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(datetime.datetime.now().strftime(
            "%Y-%m-%d")+" "+config.end_time, "%Y-%m-%d %H:%M:%S")
        now = datetime.datetime.now()
        if start_time > end_time:
            if now < end_time:
                start_time = start_time + datetime.timedelta(days=-1)
            else:
                end_time = end_time + datetime.timedelta(days=1)

        if not (start_time < datetime.datetime.now() < end_time):
            return True

        if not self.last_check_date is None and config.frequency*1000+self.last_check_date > current:
            return True
        if self.pending:
            return True
        self.pending = True
        self.last_check_date = getTime()
        self.logger.info("{name}检查开始".format(name=config.name))
        check_time = None
        try:
            start = getTime()
            self._do_health()
            end = getTime()
            check_time = end-start
            if eval(str(check_time)+config.timeout_rel + str(config.timeout*1000)) and not config.ignore_timeout_error:
                raise HealthError("响应结果超时")
            self._reset_fail_count()
            self.logger.info("{name}检查通过, 响应时间: {check_time}".format(
                name=config.name, check_time=check_time))
        except (HealthError, BaseException) as err:
            reason = err.args[0]
            self.logger.error("{name}检查失败, 响应时间: {check_time}, 错误原因: {error_msg}".format(
                name=config.name, check_time=check_time, error_msg=reason))
            self.fail_count = self.fail_count+1
            if self.fail_count >= config.fail_notify_count:
                if isinstance(err, HealthError):
                    self.notify(reason, err.selected_receiver)
                else:
                    self.notify(reason)
            return False
        finally:
            self.pending = False
        return True

    def _reset_fail_count(self):
        if self.fail_notify_count > 0:
            content = "{name}恢复正常".format(name=self.config.name)
            if self.last_receives is not None and len(self.last_receives) > 0:
                NotifyManager().send_groups_text(self.last_receives, content)
        self.fail_count = 0
        self.fail_notify_count = 0
        self.last_fail_notify_date = None

    def notify(self, reason, selected_receiver=None):
        if not self.last_fail_notify_date is None and \
                self.last_fail_notify_date+self.config.fail_silent_period*1000 > getTime():
            return
        self.last_fail_notify_date = getTime()
        content = "{name}发生异常, 连续{fail_count}次未通过健康检查,原因: {reason}".format(
            name=self.config.name, fail_count=self.fail_count, reason=reason)
        self.logger.error(content)
        self.fail_notify_count = self.fail_notify_count + 1
        if self.config.receivers is not None and len(self.config.receivers) > 0:
            if selected_receiver is None:
                self.last_receives = self.config.receivers
                NotifyManager().send_groups_text(self.last_receives, content)
            else:
                self.last_receives = list(
                    filter(lambda x: x == selected_receiver, self.config.receivers))
                NotifyManager().send_groups_text(self.last_receives, content)

    def load_import(self):
        config = self.config
        if len(config.imports) > 0:
            for import_cls in config.imports:
                exec("global {import_cls};import {import_cls};".format(
                    import_cls=import_cls))

    @abstractmethod
    def _do_health(self):
        pass
