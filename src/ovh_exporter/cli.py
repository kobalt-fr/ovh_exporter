"""Command line entry-points."""
import logging
import time

import click
from prometheus_client import start_http_server, REGISTRY
import yaml

from .ovh_client import Configuration, fetch, build_client
from .logger import init_logging
from .collector import OvhCollector


@click.group("ovh_exporter")
def main():
    """Command line entry-point."""
    init_logging(logging.INFO)


@main.command("ovh")
def ovh():
    """OVH client test."""
    with open("config.yaml", encoding="utf-8") as fstream:
        config_dict = yaml.safe_load(fstream)
    service_id = config_dict["services"][0]["id"]
    client = build_client(Configuration.load(config_dict["ovh"]))
    fetch(client, service_id)


@main.command("server")
def server():
    """Exporter startup"""
    with open("config.yaml", encoding="utf-8") as fstream:
        config_dict = yaml.safe_load(fstream)
    service_id = config_dict["services"][0]["id"]
    client = build_client(Configuration.load(config_dict["ovh"]))
    REGISTRY.register(OvhCollector(client, service_id))
    start_http_server(9100)
    while True:
        time.sleep(5)
