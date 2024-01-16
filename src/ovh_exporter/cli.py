"""Command line entry-points."""
import logging
import os
import os.path
import sys

import click
import dotenv
import yaml
from prometheus_client import REGISTRY
from prometheus_client.exposition import make_wsgi_app

from ovh_exporter import auth
from ovh_exporter.collector import OvhCollector
from ovh_exporter.config import Config, expandvars, validate
from ovh_exporter.logger import init_logging, log
from ovh_exporter.ovh_client import build_client, fetch
from ovh_exporter.wsgi import BasicAuthMiddleware, run_server

VERBOSITY = {
    "info": logging.INFO,
    "debug": logging.DEBUG,
    "warning": logging.WARNING,
    "error": logging.ERROR
}

@click.group("ovh_exporter")
@click.option("-v", "--verbosity",
              type=click.Choice(["warning", "info", "debug", "error"]),
              default="warning",
              envvar="OVH_EXPORTER_VERBOSITY")
@click.option("-c", "--config",
              type=click.Path(exists=True, dir_okay=False),
              default="config.yaml",
              envvar="OVH_EXPORTER_CONFIG")
@click.pass_context
def main(ctx, config, verbosity):
    """Command line entry-point. Load configuration."""
    init_logging(VERBOSITY[verbosity])
    with open(config, encoding="utf-8") as fstream:
        # Load configuration
        config_dict = yaml.safe_load(fstream)
        validate(config_dict)
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
        # Set on context
        ctx.obj = Config.load(config_dict)


@main.command("ovh")
@click.pass_context
def ovh(ctx):
    """OVH client test."""
    service_id = ctx.obj.services[0].id
    client = build_client(ctx.obj.ovh)
    fetch(client, service_id)


@main.command("server")
@click.pass_context
def server(ctx):
    """Exporter startup"""
    # load client
    client = build_client(ctx.obj.ovh)
    # initialize registry
    REGISTRY.register(OvhCollector(client, ctx.obj.services))
    scheme = "http"
    tls = ctx.obj.server.tls
    cert_file = None
    key_file = None
    if tls.enabled:
        if (
            not tls.cert_file
            or not tls.key_file):
            print("TLS enabled but server.tls.(cert_file|key_file) configurations are missing.", file=sys.stderr) # noqa: T201
            ctx.exit(1)
        if (
            not os.path.exists(tls.cert_file)
            or not os.path.exists(tls.key_file)):
            print(f"TLS enabled but {tls.cert_file} or {tls.key_file} file are mssing.", file=sys.stderr) # noqa: T201
            ctx.exit(1)
        scheme = "https"
        cert_file = tls.cert_file
        key_file = tls.key_file
    basic_auth = ctx.obj.server.basic_auth
    wsgi_app = make_wsgi_app(REGISTRY)
    if basic_auth.enabled:
        if not basic_auth.login or not basic_auth.password:
            print("Login and password for basic auth are missing.", file=sys.stderr) # noqa: T201
            ctx.exit(1)
        wsgi_app = BasicAuthMiddleware(
            wsgi_app,
            basic_auth.login,
            basic_auth.password
        )
    bind_addr = ctx.obj.server.bind_addr
    bind_port = ctx.obj.server.port
    print(f"Visit {scheme}://{bind_addr}:{bind_port}/metrics to view metrics.") # noqa: T201
    run_server(wsgi_app,
               bind_addr, bind_port,
               cert_file, key_file)


@main.command("login")
@click.pass_context
def login(ctx):
    """Perform login (retrieve consumerKey). Updated env_file if configured."""
    auth.login(ctx.obj)

