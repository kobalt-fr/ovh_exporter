"""Configuration loading utilities."""
from __future__ import annotations

import os
import string
import typing

import yaml
from jsonschema import Draft202012Validator
from referencing import Registry

CONFIG_SCHEMA = """
$schema: https://json-schema.org/draft/2020-12/schema
title: ovh_exporter configuration
type: object
properties:
  ovh:
    description: OVH account credentials
    type: object
    $ref: urn:OvhAccount
  env_file:
    description: Environment variables file path
    type: string
  services:
    description: OVH project/service to check
    type: array
    items:
      type: object
      $ref: urn:Service
required:
  - ovh
  - services
"""
SERVICE_SCHEMA = """
$schema: https://json-schema.org/draft/2020-12/schema
title: OVH project/service
type: object
properties:
  id:
    description: Service id
    type: string
    pattern: ^[a-f0-9]{32}$
  labels:
    description: Prometheus labels to apply to related metrics
    type: object
    patternProperties:
      "^[a-zA-Z0-9_:]+$":
        type: string
    additionalProperties: false
required:
  - id
"""
OVH_ACCOUNT_SCHEMA = """
$schema: https://json-schema.org/draft/2020-12/schema
title: OVH account
type: object
properties:
  endpoint:
    description: API endpoint (ovh-eu, ovh-ca, ...)
    type: string
    enum:
      - ovh-eu
      - ovh-us
      - ovh-ca
      - soyoustart-eu
      - soyoustart-ca
      - kimsufi-eu
      - kimsufi-ca
  application_key:
    description: Application key
    type: string
  application_secret:
    description: Application secret
    type: string
  consumer_key:
    description: Consumer key; use ${ENV_VAR} to reference an environment variable
    type: string
required:
  - endpoint
  - application_key
  - application_secret
"""
SERVER_SCHEMA = """
$schema: https://json-schema.org/draft/2020-12/schema
title: HTTP server setting
type: object
properties:
  port:
    type: integer
    description: Listen port for server
  tls:
    description: TLS setting
    type: object
    properties:
      enabled:
        type: boolean
        description: Enable TLS
        default: false
      cert_file:
        type: string
        description: Certificate file
      key_file:
        type: string
        description: Key file
  basic_auth:
    description: Basic authentication setting
    type: object
    properties:
      enabled:
        type: boolean
        default: false
      login:
        type: string
        description: Basic authentication login
      password:
        type: string
        description: Basic authentication password
"""

REGISTRY: Registry = Registry().with_contents([
    ("urn:Config", yaml.safe_load(CONFIG_SCHEMA)),
    ("urn:OvhAccount", yaml.safe_load(OVH_ACCOUNT_SCHEMA)),
    ("urn:Service", yaml.safe_load(SERVICE_SCHEMA)),
    ("urn:Server", yaml.safe_load(SERVER_SCHEMA))
])


# pylint: disable=too-few-public-methods
class OvhAccount:
    """OVH account configuration."""
    def __init__(
        self,
        endpoint: str,
        application_key: str,
        application_secret: str,
        consumer_key: str|None,
    ):
        self.endpoint = endpoint
        self.application_key = application_key
        self.application_secret = application_secret
        self.consumer_key = consumer_key

    @staticmethod
    def load(config_dict):
        """Load configuration from a configuration dict."""
        validator = Draft202012Validator(
            REGISTRY.contents("urn:OvhAccount"),
            registry=REGISTRY
        )
        validator.validate(config_dict)
        return OvhAccount(
            config_dict["endpoint"],
            config_dict["application_key"],
            config_dict["application_secret"],
            config_dict.get("consumer_key", None),
        )


class Tls:
    """TLS options."""
    def __init__(
            self,
            enabled: bool, # noqa: FBT001
            cert_file: str|None,
            key_file: str|None):
        self.enabled = enabled
        self.cert_file = cert_file
        self.key_file = key_file

    @staticmethod
    def load(config_dict):
        """Load configuration from dict."""
        enabled = config_dict.get("enabled", False)
        return Tls(
            enabled,
            config_dict.get("cert_file", None),
            config_dict.get("key_file", None)
        )


class BasicAuth:
    """Basic authentication options."""
    def __init__(
            self,
            enabled: bool, # noqa: FBT001
            login: str|None,
            password: str|None):
        self.enabled = enabled
        self.login = login
        self.password = password

    @staticmethod
    def load(config_dict):
        """Load configuration from dict."""
        enabled = config_dict.get("enabled", False)
        return BasicAuth(
            enabled,
            config_dict.get("login", None),
            config_dict.get("password", None)
        )


class Server:
    """Server configuration."""
    def __init__(
            self,
            bind_addr: str,
            port: int,
            tls: Tls,
            basic_auth: BasicAuth):
        self.port = port
        self.bind_addr = bind_addr
        self.tls = tls
        self.basic_auth = basic_auth

    @staticmethod
    def load(config_dict):
        """Load server configuration."""
        bind_addr = config_dict.get("bind_addr", "localhost")
        port = config_dict.get("port", 9100)
        basic_auth = BasicAuth.load(config_dict.get("basic_auth", {}))
        tls = Tls.load(config_dict.get("tls", {}))
        return Server(bind_addr, port, tls, basic_auth)


class Service:
    """Configuration."""
    def __init__(
            self,
            field_id: str,
            labels: typing.Mapping[str, str]):
        self.id = field_id
        self.labels = labels

    @staticmethod
    def load(config_dict):
        """Load service."""
        return Service(config_dict["id"], config_dict.get("labels", {}))


class Config:
    """Configuration."""
    def __init__(
            self,
            ovh: OvhAccount,
            server: Server,
            env_file: str,
            services: list[Service]):
        self.ovh = ovh
        self.server = server
        self.env_file = env_file
        self.services = services

    @staticmethod
    def load(config_dict):
        """Load whole configuration."""
        validator = Draft202012Validator(
            REGISTRY.contents("urn:Config"),
            registry=REGISTRY
        )
        validator.validate(config_dict)
        ovh = OvhAccount.load(config_dict.get("ovh"))
        server = Server.load(config_dict.get("server", {}))
        services = [
            Service.load(i)
            for i in config_dict.get("services", [])]
        return Config(ovh,
                      server,
                      config_dict.get("env_file", None),
                      services)


def validate(config_dict):
    """Validation configuration."""
    validator = Draft202012Validator(
        REGISTRY.contents("urn:Config"),
        registry=REGISTRY
    )
    validator.validate(config_dict)


def expandvars(dictionary):
    """Expand environment variable in dictionary."""
    for k, v in dictionary.items():
        if isinstance(v, dict):
            expandvars(v)
        elif isinstance(v, str):
            dictionary[k] = string.Template(v).substitute(os.environ)
