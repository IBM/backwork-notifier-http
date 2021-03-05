"""Backwork plug-in for HTTP notifications. 
"""

import requests
import json
import re

class HTTPRequestNotifier(object):  # pylint: disable=unused-variable
    """Trigger an HTTP request with backwork-notifier-http"""

    command = "http"

    def __init__(self, args, extra):
        """Initialize HTTP notifier with client"""
        self.args = args
        self.extra = extra

    @classmethod
    def parse_args(cls, parser):
        """Add command line argument parsing rules for notifications via HTTP requests."""
        parser.add_argument(
            "--http-notifier-url",
            required=False,
            help="""The URL to be targeted as the HTTP request endpoint""",
        )
        parser.add_argument(
            "--http-notifier-bearer",
            required=False,
            help="""If set, this value will be used as an Authorization Bearer token and sent with the HTTP request.""",
        )
        parser.add_argument(
            "--http-notifier-basic-user",
            required=False,
            help="""If set, this value (along with --http-notifier-basic-pass) will be used for basic auth and sent with the HTTP request.""",
        )
        parser.add_argument(
            "--http-notifier-basic-pass",
            required=False,
            help="""If set, this value (along with --http-notifier-basic-user) will be used for basic auth and sent with the HTTP request.""",
        )
        parser.add_argument(
            "--http-notifier-method",
            required=False,
            help="""The method to be used for the HTTP request. Choose from 'post' or 'get'. Default is 'post'.""",
        )
        parser.add_argument(
            "--http-notifier-data",
            required=False,
            help="""JSON string sent as the 'data' object with the HTTP request. Format as the following: '{"key": "value"}' """,
        )
        parser.add_argument(
            "--http-notifier-params",
            required=False,
            help="""JSON string with params to be sent with the HTTP request.""",
        )
        parser.add_argument(
            "--http-notifier-add-headers",
            required=False,
            help="""JSON string with headers to be sent with the HTTP request. 
                    For authorization, use --http-notifier-bearer or --http-notifier-basic-user & --http-notifier-basic-pass.""",
        )
        parser.add_argument(
            "--http-notifier-key",
            required=False,
            help="""The key name for the error message (from backwork) that is appended to the 'data' (--http-notifier-data) object. 
                    Use '.' to traverse the JSON tree (up to 6 levels deep). For example, --http-notifier-key="data.error.message" is 3 levels deep. 
                    By default, if no key is specified the error message will not be appended.""",
        )

    def log(self, msg=""):
        print("[backwork-notifier-http]: {}".format(msg))

    def addKeyToObject(self, key="", msg="", data={}):
        if len(key) == 0:
            return data

        try:
            paths = key.split(".")
            length = len(paths)
            if length == 6:
                data[paths[0]][paths[1]][paths[2]][paths[3]][paths[4]][paths[5]] = "{}".format(msg)
            elif length == 5:
                data[paths[0]][paths[1]][paths[2]][paths[3]][paths[4]] = "{}".format(msg)
            elif length == 4:
                data[paths[0]][paths[1]][paths[2]][paths[3]] = "{}".format(msg)
            elif length == 3:
                data[paths[0]][paths[1]][paths[2]] = "{}".format(msg)
            elif length == 2:
                data[paths[0]][paths[1]] = "{}".format(msg)
            elif length == 1:
                data[paths[0]] = "{}".format(msg)
        except Exception as e:
            self.log(
                "Can't attach backwork error message to data object for HTTP request. Reason: {}".format(
                    str(e)
                )
            )

        return data

    def formatJson(self, data):
        return str(data).strip("'<>() ").replace("'", '"')

    def redaction(self, msg):
        REDACTED = '[REDACTED]'

        try:
            msg = str(msg)
            credentials = re.search('(?<=:\/\/).*(?=@)', msg)
            if credentials:
                credentials = credentials.group().split(':')
                msg = msg.replace(credentials[0], REDACTED)
                msg = msg.replace(credentials[1], REDACTED)
            else: 
                credentials = re.findall("(?<=\s)'\w+'", msg)
                if credentials: 
                    msg = msg.replace(credentials[0], REDACTED)
                    msg = msg.replace(credentials[1], REDACTED)

        except Exception as e:
            self.log("Unable to redact credentials... Error: {}".format(str(e)))

        return msg

    def notify(self, msg=""):
        """Notify an HTTP endpoint."""

        url = self.args.http_notifier_url or ""
        method = self.args.http_notifier_method or "post"
        key = self.args.http_notifier_key or ""
        bearer = self.args.http_notifier_bearer or ""
        basicUser = self.args.http_notifier_basic_user or ""
        basicPass = self.args.http_notifier_basic_pass or ""

        _data = self.args.http_notifier_data or ""
        data = {}
        _params = self.args.http_notifier_params or ""
        params = {}
        _additionalHeaders = self.args.http_notifier_add_headers or ""

        prelimHeaders = {"Content-Type": "application/json"}
        additionalHeaders = {}

        # convert to data to Python dict
        if len(_data) > 0:
            try:
                data = json.loads(self.formatJson(_data))
            except Exception as e:
                self.log(
                    "Invalid object sent as --http-notifier-data. Message: {}".format(
                        str(e)
                    )
                )

        if len(_params) > 0:
            try:
                params = json.loads(self.formatJson(_params))
            except Exception as e:
                self.log(
                    "Invalid object sent as --http-notifier-params. Message: {}".format(
                        str(e)
                    )
                )

        # add authorization token if applicable
        if len(bearer) > 0:
            prelimHeaders["Authorization"] = "Bearer {}".format(bearer)

        if len(_additionalHeaders) > 0:
            try:
                additionalHeaders = json.loads(self.formatJson(_additionalHeaders))
            except Exception as e:
                self.log(
                    "Invalid object sent as --http-notifier-add-headers. Message: {}".format(
                        str(e)
                    )
                )

        # redact service credentials.
        msg = self.redaction(msg)

        # attach msg to data object to be sent
        data = self.addKeyToObject(key, msg, data)

        # merge headers
        headers = {**prelimHeaders, **additionalHeaders}

        try:
            self.log("Performing '{}' request on {}".format(method, url))
            x = None
            if "get" in method:
                if len(basicUser) > 0 and len(basicPass) > 0:
                    x = requests.get(
                        url,
                        params=params,
                        data=json.dumps(data),
                        headers=headers,
                        auth=(basicUser, basicPass),
                    )
                else:
                    x = requests.get(
                        url, params=params, data=json.dumps(data), headers=headers
                    )
            elif "post" in method:
                if len(basicUser) > 0 and len(basicPass) > 0:
                    x = requests.post(
                        url,
                        params=params,
                        data=json.dumps(data),
                        headers=headers,
                        auth=(basicUser, basicPass),
                    )
                else:
                    x = requests.post(
                        url, params=params, data=json.dumps(data), headers=headers
                    )
            else:
                self.log(
                    "Invalid method: '{}'. Please see the help menu for --http-notifier-method.".format(
                        method
                    ),
                )

            if x is not None:
                self.log("Response: {}".format(str(x.status_code)))
                if x.status_code >= 199 and x.status_code < 300:
                    self.log(x.json())
                else:
                    self.log(x.text)

        except Exception as e:
            self.log(
                "An error occured during the request to {}. Message: {}".format(
                    url, str(e)
                )
            )
