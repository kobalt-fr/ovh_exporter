"""Command line entry-points."""
import logging
import os
import os.path
import pathlib
import string
import sys

import click
import dotenv
from prometheus_client import REGISTRY
from prometheus_client.twisted import MetricsResource
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, ssl
import yaml

from . import auth
from .collector import OvhCollector
from .logger import init_logging, log
from .ovh_client import Configuration, fetch, build_client

VERBOSITY = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

@click.group("ovh_exporter")
@click.option("-v", "--verbosity",
              type=click.Choice(["warning", "info", "debug", "error"]),
              default="warning")
@click.pass_context
def main(ctx, verbosity):
    """Command line entry-point. Load configuration."""
    init_logging(VERBOSITY[verbosity])
    with open("config.yaml", encoding="utf-8") as fstream:
        # Load configuration
        config_dict = yaml.safe_load(fstream)
        # Set on context
        ctx.obj = config_dict
        # Load environment file if provided
        if (
            "env_file" in config_dict
            and config_dict["env_file"]
            and os.path.exists(config_dict["env_file"])
        ):
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
@click.option("--tls-cert-file", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
@click.option("--tls-key-file", type=click.Path(exists=True, dir_okay=False, path_type=pathlib.Path))
@click.pass_context
def server(ctx, tls_cert_file, tls_key_file):
    """Exporter startup"""
    # load client
    config_dict = ctx.obj
    client = build_client(Configuration.load(config_dict["ovh"]))
    # initialize registry
    REGISTRY.register(OvhCollector(client, config_dict["services"]))
    # load optional TLS certificate
    certificate = None
    if tls_cert_file or tls_key_file:
        if not (tls_cert_file and tls_key_file):
            print("Both --tls-*-file options are needed.", file=sys.stderr)
            sys.exit(1)
        cert = tls_cert_file.read_text(encoding="utf-8")
        key = tls_key_file.read_text(encoding="utf-8")
        data = cert + "\n" + key
        certificate = ssl.PrivateCertificate.loadPEM(data)
    # start HTTP(s) server
    root = Resource()
    root.putChild(b'metrics', MetricsResource())
    factory = Site(root)
    port = 9100
    if certificate:
        log.info("Using TLS server.")
        # pylint: disable=E1101:no-member
        scheme = "https"
        reactor.listenSSL(port, factory, certificate.options())
    else:
        scheme = "http"
        # pylint: disable=E1101:no-member
        reactor.listenTCP(port, factory)
    print(f"Visit {scheme}://localhost:{port}/metrics to view metrics.")
    # pylint: disable=E1101:no-member
    reactor.run()


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
