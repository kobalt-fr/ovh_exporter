# ovh_exporter

## Purpose

`ovh_exporter` allows to expose consumption data about your OVH public cloud projects in a format compatible with prometheus.

`ovh_exporter` can be configured to use TLS (https) protocol and basic authentication.

OVH credentials used by `ovh_exporter` can be restricted only to needed API paths and methods.

As collecting all OVH metrics can be slow, and collected metrics are moderately dynamic, you should configure a long delay between prometheus scrape (> minutes).

## Installation

```
# Build
hatch build
# Install
pip install dist/*.whl
# Usage
ovh_exporter --help
```

## Usage

Copy and modify `config.yaml.tmpl` with:
* OVH API credentials (`ovh.*`)
* OVH project identifiers (`services[].*`)

```
ovh_exporter -c config.yaml server
```

## Configuration

### Enable TLS

```yaml
server:
  tls:
    enabled: true
    cert_file: cert/file/path.pem
    key_file: key/file/path
```

`certificates/*` files are provided for testing and developing purpose. Do not reuse.

### Enable basic authentication

```yaml
server:
  basic_auth:
    enabled: true
    login: login
    password: password
```

### Server binding

```yaml
server:
  bind_addr: localhost
  port: 9100
```

### Custom labels

Each OVH project can be bound to custom labels:

```yaml
services:
- id: a2a57ad2af1e382a46d65b5e3bd2945a
  labels:
    label1: value1
    label2: value2
```

### Use environment variables

You can use `${VAR_NAME}` to reference environment variable inside configuration.

## OVH API client

You can create both `application_key`, `application_secret` and `consumer_key` at
https://www.ovh.com/auth/api/createToken.

With an existing `application_key` and `application_secret`, you can obtain a `consumer_key` with the `ovh login` command. It allows to restrict authorized paths and methods strictly to the needed one.

## Metrics

`ovh_exporter` provides data about:

* object storage
  * storage consumption / price (gb.hour) (2 metrics)
  * external / external - inconming / outgoing bandwidth - consumption / price (8 metrics)
* volumes
  * size (gb)
* quota (current / max)
  * volume size
  * volume backup
  * volume count
  * volume backup count
  * instance count
  * cpu count
  * ram (gb)
  * network count
  * network subnet count
  * network floating ip count
  * network gateway count
  * load balancer count
  * key manager count
* storage
  * size
  * object count
* instance usage
  * hours
  * price
* volume
  * gb x hours consumption
  * price

## Build a docker image

```
# Build image
docker build -t ovh_exporter .
# Run with a local config
docker run --rm \
  -e OVH_EXPORTER_CONFIG=/app/config.yaml \
  -v $PWD/config.yaml:/app/config.yaml \
  -v $PWD/auth.env:/app/auth.env \
  -v $PWD/certificates:/app/certificates \
  ovh_exporter
```

## History

### v0.1 (2023-01-16)

* initial release
