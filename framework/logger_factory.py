import os
from time import gmtime, strftime
import logging

from logging import handlers


_level_relations = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}  # 日志级别关系映射


def Logger(name, module, level='debug', when='D', backCount=3):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    filename = os.path.join("logs", name+'.log')
    fmt = '%(asctime)s - '+module + \
        '[line:%(lineno)d] - %(levelname)s: %(message)s'
    logger = logging.getLogger(filename)
    format_str = logging.Formatter(fmt)  # 设置日志格式
    logger.setLevel(_level_relations.get(level))  # 设置日志级别
    sh = logging.StreamHandler()  # 往屏幕上输出
    sh.setFormatter(format_str)  # 设置屏幕上显示的格式
    th = handlers.TimedRotatingFileHandler(
        filename=filename,
        when=when,
        backupCount=backCount,
        encoding='utf-8'
    )  # 往文件里写入#指定间隔时间自动生成文件的处理器
    # 实例化TimedRotatingFileHandler
    # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
    # S 秒
    # M 分
    # H 小时、
    # D 天、
    # W 每星期（interval==0时代表星期一）
    # midnight 每天凌晨
    th.setFormatter(format_str)  # 设置文件里写入的格式
    logger.addHandler(sh)  # 把对象加到logger里
    logger.addHandler(th)
    return logger
