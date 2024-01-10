"""Configuration loading utilities."""
import os
import string

from jsonschema import Draft202012Validator
from referencing import Registry
import yaml

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
  - consumer_key
"""

REGISTRY = Registry().with_contents([
    ("urn:Config", yaml.safe_load(CONFIG_SCHEMA)),
    ("urn:OvhAccount", yaml.safe_load(OVH_ACCOUNT_SCHEMA)),
    ("urn:Service", yaml.safe_load(SERVICE_SCHEMA))
])

# pylint: disable=too-few-public-methods
class OvhAccount:
    """OVH account configuration."""

    def __init__(
        self,
        endpoint: str,
        application_key: str,
        application_secret: str,
        consumer_key: str,
    ):
        self.endpoint = endpoint
        self.application_key = application_key
        self.application_secret = application_secret
        self.consumer_key = consumer_key

    @staticmethod
    def load(config_dict, consumer_key_optional=False):
        """Load configuration from a configuration dict."""
        schema = yaml.safe_load(OVH_ACCOUNT_SCHEMA)
        if consumer_key_optional:
            schema["required"].remove("consumer_key")
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
