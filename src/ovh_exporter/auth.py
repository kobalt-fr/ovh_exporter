"""OVH authentication utility."""
import datetime
import fileinput
import http.server
import os.path
import re
import subprocess
import threading

import ovh

from .config import OvhAccount
from .logger import log


def login(config_dict, account: OvhAccount):
    """Init an auth process. Consumer key is displayed in console and
    `env_file` is updated if provided (replace any OVH_CONSUMER_KEY
    declaration)."""
    client = ovh.Client(
        endpoint=account.endpoint,
        application_key=account.application_key,
        application_secret=account.application_secret,
    )
    req = ovh.ConsumerKeyRequest(client=client)
    req.add_rule("GET", "/me")
    for service in config_dict["services"]:
        req.add_rule("GET", f"/cloud/project/{service['id']}")
        req.add_rule("GET", f"/cloud/project/{service['id']}/quota")
        req.add_rule("GET", f"/cloud/project/{service['id']}/instance")
        req.add_rule("GET", f"/cloud/project/{service['id']}/storage")
        req.add_rule("GET", f"/cloud/project/{service['id']}/usage/current")
        req.add_rule("GET", f"/cloud/project/{service['id']}/volume")
    pending_request = req.request("http://localhost:8000/")
    subprocess.check_call(["xdg-open", pending_request["validationUrl"]])
    print(f"Perform login in opened browser ({pending_request['validationUrl']})")
    log.debug("HTTP server starting.")
    callback_called = threading.Semaphore(1)
    httpd = http.server.HTTPServer(
        ("", 8000), CallbackHttpRequestHanderFactory(callback_called)
    )
    # pylint: disable=consider-using-with
    callback_called.acquire()

    def login_callback_server():
        httpd.serve_forever()
        log.debug("HTTP server loop ended.")

    thread = threading.Thread(name="login-callback", target=login_callback_server)
    thread.daemon = True
    thread.start()
    log.debug("HTTP server started.")
    # wait that callback page is called
    # pylint: disable=consider-using-with
    callback_called.acquire()
    log.debug("HTTP server - callback notification received.")
    httpd.shutdown()
    log.debug("HTTP server stopped.")
    consumer_key = pending_request["consumerKey"]
    print(f"Login success; consumerKey={consumer_key}")
    if "env_file" in config_dict and config_dict["env_file"]:
        update_env_file(config_dict["env_file"], consumer_key)


def update_env_file(env_file, consumer_key):
    """Update environment file with updated OVH_CONSUMER_KEY.

    A new file is created if it does not exists."""
    # create an empty file if it does not exists
    if not os.path.exists(env_file):
        with open(env_file, mode="tw", encoding="UTF-8") as f:
            f.write("OVH_CONSUMER_KEY=")
    # update OVH_CONSUMER_KEY
    with fileinput.FileInput([env_file], inplace=True) as f:
        for line in f:
            # add an 'updated on' comment
            if f.isfirstline():
                update_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"# updated on {update_str}")
            # ignore existing 'updated on' line
            if re.match(r"# updated on .*", line):
                continue
            # replace OVH_CONSUMER_KEY= definition, else keep entry
            line = re.sub(
                r"(OVH_CONSUMER_KEY *= *)(.*)", f"OVH_CONSUMER_KEY={consumer_key}", line
            )
            print(line, end="")
    print("auth.env updated.")


# pylint: disable=too-few-public-methods
class CallbackHttpRequestHanderFactory:
    """Init a CallbackHttpRequestHander with a semaphore."""

    def __init__(self, semaphore):
        self._semaphore = semaphore

    def __call__(self, *args, **kwargs):
        override = dict(kwargs)
        override["semaphore"] = self._semaphore
        return CallbackHttpRequestHandler(*args, **override)


class CallbackHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    """Callback for local http server."""

    def __init__(self, *args, **kwargs):
        override = dict(kwargs)
        self._semaphore = override["semaphore"]
        override.pop("semaphore")
        super().__init__(*args, **override)

    # pylint: disable=invalid-name
    def do_GET(self):
        """Target for redirect url.

        When response is received, we consider consumerKey is validated."""
        self.send_response(http.server.HTTPStatus.OK)
        self.send_header("Content-Type", "text/plain;charset=utf-8")
        self.end_headers()
        self.wfile.writelines(
            ["Login success! Go back to your terminal.".encode("utf-8")]
        )
        self._semaphore.release()
        log.debug("HTTP server - callback notification sent.")
