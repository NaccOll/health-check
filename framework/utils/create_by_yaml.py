import os
import yaml

from ..struct.dict import Dict


def create_by_yaml(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("app config file not exists")
    with open(file_path, 'r', encoding='UTF-8') as file_ptr:
        config = yaml.load(file_ptr, yaml.SafeLoader)
    return Dict.create(config)
