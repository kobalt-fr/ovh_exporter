"""Command line entry-points."""
import logging
import os
import os.path
import string
import time

import click
import dotenv
from prometheus_client import start_http_server, REGISTRY
import yaml

from . import auth
from .collector import OvhCollector
from .logger import init_logging, log
from .ovh_client import Configuration, fetch, build_client


@click.group("ovh_exporter")
@click.pass_context
def main(ctx):
    """Command line entry-point. Load configuration."""
    init_logging(logging.INFO)
    with open("config.yaml", encoding="utf-8") as fstream:
        # Load configuration
        config_dict = yaml.safe_load(fstream)
        # Set on context
        ctx.obj = config_dict
        # Load environment file if provided
        if "env_file" in config_dict and \
                config_dict["env_file"] and \
                os.path.exists(config_dict["env_file"]):
            env_file = config_dict["env_file"]
            log.info("Loading environment file %s", env_file)
            dotenv.load_dotenv(env_file)
        # Expand environment variables in config
        expandvars(config_dict)


@main.command("ovh")
@click.pass_context
def ovh(ctx):
    """OVH client test."""
    config_dict = ctx.obj
    service_id = config_dict["services"][0]["id"]
    client = build_client(Configuration.load(config_dict["ovh"]))
    fetch(client, service_id)


@main.command("server")
@click.pass_context
def server(ctx):
    """Exporter startup"""
    config_dict = ctx.obj
    service_id = config_dict["services"][0]["id"]
    client = build_client(Configuration.load(config_dict["ovh"]))
    REGISTRY.register(OvhCollector(client, service_id))
    start_http_server(9100)
    while True:
        time.sleep(5)


@main.command("login")
@click.pass_context
def login(ctx):
    """Perform login (retrieve consumerKey). Updated env_file if configured."""
    config_dict = ctx.obj
    auth.login(config_dict)


def expandvars(dictionary):
    """Expand environment variable in dictionary."""
    for k, v in dictionary.items():
        if isinstance(v, dict):
            expandvars(v)
        elif isinstance(v, str):
            dictionary[k] = string.Template(v).substitute(os.environ)
