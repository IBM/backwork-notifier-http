# backwork-notifier-http
Support for HTTP notifications on [backwork](https://github.com/IBM/backwork).

<!-- # backwork-notifier-sentry [![Build Status](https://travis-ci.org/IBM/backwork-notifier-sentry.svg?branch=master)] [![PyPI version](https://badge.fury.io/py/backwork-notifier-sentry.svg)](https://badge.fury.io/py/backwork-notifier-sentry)(https://travis-ci.org/IBM/backwork-notifier-sentry) -->

## Installing
You can use `pip` to install this plug-in directly:
```sh
$ pip install backwork-notifier-http
```

## Using
After installing the plug-in you will be able to use the `-n http`
argument on `backwork` commands.

```sh
$ backwork --help
usage: backwork [-h] [-n NOTIFIERS] [--http-notifier-url HTTP_NOTIFIER_URL]
                [--http-notifier-bearer HTTP_NOTIFIER_BEARER]
                [--http-notifier-basic-user HTTP_NOTIFIER_BASIC_USER]
                [--http-notifier-basic-pass HTTP_NOTIFIER_BASIC_PASS]
                [--http-notifier-method HTTP_NOTIFIER_METHOD]
                [--http-notifier-data HTTP_NOTIFIER_DATA]
                [--http-notifier-params HTTP_NOTIFIER_PARAMS]
                [--http-notifier-add-headers HTTP_NOTIFIER_ADD_HEADERS]
                [--http-notifier-key HTTP_NOTIFIER_KEY]
                {backup,restore,upload,show,download} ...

positional arguments:
  {backup,restore,upload,show,download}

optional arguments:
  -h, --help            show this help message and exit
  -n NOTIFIERS, --notify NOTIFIERS
                        enable a notifier, it can be used multiple times
  --http-notifier-url HTTP_NOTIFIER_URL
                        The URL to be targeted as the HTTP request endpoint
  --http-notifier-bearer HTTP_NOTIFIER_BEARER
                        If set, backwork will use this token value for the HTTP
                        request authorization header.
  --http-notifier-basic-user HTTP_NOTIFIER_BASIC_USER
                        If set, backwork will use this value (along with --http-
                        notifier-basic-pass) for the HTTP request basic
                        authorization.
  --http-notifier-basic-pass HTTP_NOTIFIER_BASIC_PASS
                        If set, backwork will use this value (along with --http-
                        notifier-basic-user) for the HTTP request basic
                        authorization.
  --http-notifier-method HTTP_NOTIFIER_METHOD
                        The method to be used for the HTTP request. Default is
                        'POST'.
  --http-notifier-data HTTP_NOTIFIER_DATA
                        Data (JSON string) sent with the HTTP request
  --http-notifier-params HTTP_NOTIFIER_PARAMS
                        HTTP params (JSON string) to be sent with a GET request
  --http-notifier-add-headers HTTP_NOTIFIER_ADD_HEADERS
                        JSON String with additional headers to be sent with the
                        HTTP request. For authorization, use --http-notifier-bearer
                        or --http-notifier-basic-user & --http-notifier-basic-pass.
  --http-notifier-key HTTP_NOTIFIER_KEY
                        The key name for the error message (from backwork) that is
                        appended to the 'data' (--http-notifier-data) object. Use
                        '.' to traverse the JSON tree (up to 5 levels deep). For
                        example, --http-notifier-key="data.error.message" is 3
                        levels deep. By default, if no key is specified the error
                        message will not be appended.
```
