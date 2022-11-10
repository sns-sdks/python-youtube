import json

import pytest

from pyyoutube import Client


class Helpers:
    @staticmethod
    def load_json(filename):
        with open(filename, "rb") as f:
            return json.loads(f.read().decode("utf-8"))

    @staticmethod
    def load_file_binary(filename):
        with open(filename, "rb") as f:
            return f.read()


@pytest.fixture
def helpers():
    return Helpers()


@pytest.fixture(scope="class")
def authed_cli():
    return Client(access_token="access token")


@pytest.fixture(scope="class")
def key_cli():
    return Client(api_key="api key")
