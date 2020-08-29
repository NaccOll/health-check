# -*- coding: utf-8 -*-
from abc import abstractmethod

from ..metaclass.singleton_meta import SingletonMeta


class ConfigProperties(metaclass=SingletonMeta):
    def __init__(self, config=None):
        super().__init__()
        self.config = config

    @abstractmethod
    def load_config(self, config):
        pass
