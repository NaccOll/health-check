# -*- coding: utf-8 -*-
from .config import Config


def enable_configuation(prefix):
    if type(prefix) != str:
        raise TypeError('prefix is required and must be a string')

    def load_configuation(clzss):
        Config.add_sub_config(clzss, prefix)
        return clzss
    return load_configuation
