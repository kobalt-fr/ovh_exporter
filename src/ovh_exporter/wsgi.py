"""WSGI utilities."""

import base64
import binascii

import gunicorn.app.base

from ovh_exporter.logger import log


class StandaloneApplication(gunicorn.app.base.BaseApplication):
    # 'init' and 'load' methods are implemented by WSGIApplication.
    # pylint: disable=abstract-method
    """Gunicorn wrapper."""

    def __init__(self, app, bind_addr="127.0.0.1", bind_port=9100, cert_file=None, key_file=None):
        self.cert_file = cert_file
        self.key_file = key_file
        self.bind_addr = bind_addr
        self.bind_port = bind_port
        self.application = app
        super().__init__()

    def load_config(self):
        config = {}
        if self.cert_file and self.key_file:
            config["certfile"] = self.cert_file
            config["keyfile"] = self.key_file
        config["bind"] = f"{self.bind_addr}:{self.bind_port}"
        config["workers"] = 3
        config["worker_class"] = "gthread"
        config["timeout"] = 180
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


class BasicAuthMiddleware:
    """Basic Auth WSGI middleware"""

    def __init__(self, app, login, password, realm="ovh_exporter"):
        self.app = app
        self.realm = realm
        self.login = login
        self.password = password

    def __call__(self, environ, start_response):
        if not self._check_auth(environ):
            start_response("401 Unauthorized", [("WWW-Authenticate", f'Basic realm={self.realm}, charset="UTF-8"')])
            return []
        return self.app(environ, start_response)

    def _check_auth(self, environ):
        authorization = environ.get("HTTP_AUTHORIZATION", None)
        if authorization:
            auth = self._extract_authorization(authorization)
            if auth and self.login == auth[0] and self.password == auth[1]:
                return True
        return False

    def _extract_authorization(self, authorization_header: str):
        """Extract decoded Authorization."""
        if not authorization_header.startswith("Basic "):
            log.debug("Authorization is not a basic authentication.")
            return False
        try:
            # Strip 'Basic '
            authorization_base64 = authorization_header[6:].encode("ascii")
            auth = base64.decodebytes(authorization_base64).decode("utf-8")
            separator = auth.find(":")
            if separator != -1:
                return (auth[0:separator], auth[separator + 1 :])
            else:  # noqa: RET505
                log.debug("Decoded authorization cannot be parsed.")
                return False
        except binascii.Error:
            log.debug("Authorization is not a basic authentication.")
            return False


def run_server(app, bind_addr="127.0.0.1", bind_port=9100, cert_file=None, key_file=None):
    """Start a WSGI server"""
    StandaloneApplication(app, bind_addr, bind_port, cert_file, key_file).run()
