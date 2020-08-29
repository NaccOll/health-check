from typing import List
import importlib
from concurrent.futures import ThreadPoolExecutor
from framework.struct.actor import Actor
from framework.metaclass.singleton_meta import SingletonMeta
from .properties import HealthProperties
from .health.abstract_health import AbstractHealth


def build_health_checker(health_config: HealthProperties) -> List[AbstractHealth]:
    checkers: List[AbstractHealth] = []
    configs = health_config.configs
    for config in configs:
        checker_module = importlib.import_module(config.exec)
        checker_class = getattr(checker_module, config.exec_class)
        checker_instance = checker_class(config)
        checkers.append(checker_instance)
    return checkers


def trigger_check(checker: AbstractHealth) -> None:
    checker.do_health()


class HealthActor(Actor, metaclass=SingletonMeta):
    def __init__(self, config: HealthProperties):
        super().__init__()
        self.load(config)

    def load(self, config: HealthProperties):
        self.checks = build_health_checker(config)
        self.pool = ThreadPoolExecutor(len(self.checks))

    def reload(self, config):
        self.load(config)

    def run(self):
        '''
        Run method to be implemented by the user
        '''
        while True:
            msg = self.recv()
            for checker in self.checks:
                self.pool.submit(trigger_check, checker)
