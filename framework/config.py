# -*- coding: utf-8 -*-
from typing import List
import os
from enum import Enum, unique
from .utils.create_by_yaml import create_by_yaml

from .struct.dict import Dict
from .metaclass.no_instances_meta import NoInstancesMeta
from .struct.config_properties import ConfigProperties


@unique
class _ConfigLoadState(Enum):
    INIT = 0
    LOADING = 1
    DONE = 2


class Config(metaclass=NoInstancesMeta):
    _file_properties = []
    _system_env = Dict()

    _properties = None

    _subscribe_config = {}

    _load_state = _ConfigLoadState.INIT
    _config_filename = 'application'

    @staticmethod
    def load_config(profiles='', extra_config_path='extra_config'):
        Config._load_state = _ConfigLoadState.LOADING
        fixed_config_dir = 'config'
        profiles = list(map(lambda x: x.strip(), profiles.split(',')))
        Config.__load_config_by_file(fixed_config_dir, profiles)
        if fixed_config_dir != extra_config_path and os.path.exists(extra_config_path):
            Config.__load_config_by_file(extra_config_path, profiles)

        for key in os.environ:
            Config._system_env[key] = os.getenv(key)
        Config._load_state = _ConfigLoadState.DONE
        Config._load_all_sub_config()

    @staticmethod
    def __load_config_by_file(config_dir: str, profiles: List[str]):
        abs_config_dir = os.path.abspath(config_dir)
        candicate_filelist = os.listdir(config_dir)
        candicate_filepaths = map(lambda filepath: os.path.join(
            abs_config_dir, filepath), candicate_filelist)
        config_files = []
        config_filenames = [Config._config_filename]
        config_filenames.extend(list(
            map(lambda x: Config._config_filename+"-"+x, profiles)))
        for filepath in candicate_filepaths:
            if not (filepath.endswith(".yml") or filepath.endswith(".yaml")):
                continue
            basename = os.path.basename(filepath)
            if os.path.splitext(basename)[0] in config_filenames:
                config_files.append(filepath)
        for config_file in config_files:
            properties = create_by_yaml(config_file)
            Config._file_properties.append(Dict.create({
                'filename': os.path.basename(config_file),
                'properties': properties
            }))

    @staticmethod
    def properties() -> Dict:
        if Config._properties is None:
            result = Dict()
            for item in Config._file_properties:
                result.update(item.properties)
            result.update(Config._system_env)
            Config._properties = result
        return Config._properties

    @staticmethod
    def add_sub_config(cls_config: ConfigProperties, prefix):
        classname = cls_config.__module__
        Config._subscribe_config[classname] = Dict.create({
            'config': cls_config,
            'name': classname,
            'prefix': prefix
        })
        if Config._load_state == _ConfigLoadState.DONE:
            Config._load_sub_config(classname)

    @staticmethod
    def _load_all_sub_config():
        for clsname in Config._subscribe_config:
            Config._load_sub_config(clsname)

    @staticmethod
    def _load_sub_config(clsname):
        sub_config = Config._subscribe_config[clsname]
        sub_config_class = sub_config.config
        sub_config_prefix = sub_config.prefix
        sub_properties = Config.properties().get_prefix(sub_config_prefix)
        if sub_properties is None:
            return
        sub_config_instance: ConfigProperties = sub_config_class()
        sub_config_instance.load_config(sub_properties)
