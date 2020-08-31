# -*- coding: utf-8 -*-
import click
from framework import Config


@click.group()
def common():
    pass


@common.command(short_help='Bootstrap health-server.')
@click.option('--env', '-e', default='dev', help='Select mode.')
@click.option('--extra_config_path', '-c', default='extra_config', help='Use extra config path')
def start_server(env, extra_config_path):
    Config.load_config(env, extra_config_path)
    from app import run
    run()

cli = click.CommandCollection(sources=[common])

if __name__ == '__main__':
    cli()
