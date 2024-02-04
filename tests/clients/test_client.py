"""
    Tests for client.
"""

import pytest

import responses
from requests import Response, HTTPError

from .base import BaseTestCase
from pyyoutube import Client, PyYouTubeException


class TestClient(BaseTestCase):
    BASE_PATH = "testdata"
    RESOURCE = "channels"

    def test_initial(self):
        with pytest.raises(PyYouTubeException):
            Client()

        cli = Client(api_key="key", headers={"HA": "P"})
        assert cli.session.headers["HA"] == "P"

    def test_client_secret_web(self):
        filename = "apidata/client_secrets/client_secret_web.json"
        client_secret_path = f"{self.BASE_PATH}/{filename}"
        cli = Client(client_secret_path=client_secret_path)

        assert cli.client_id == "client_id"
        assert cli.client_secret == "client_secret"
        assert cli.DEFAULT_REDIRECT_URI == "http://localhost:5000/oauth2callback"

    def test_client_secret_installed(self):
        filename_good = "apidata/client_secrets/client_secret_installed_good.json"
        client_secret_good_path = f"{self.BASE_PATH}/{filename_good}"

        cli = Client(client_secret_path=client_secret_good_path)

        assert cli.client_id == "client_id"
        assert cli.client_secret == "client_secret"

    def test_client_secret_bad(self):
        filename_bad = "apidata/client_secrets/client_secret_installed_bad.json"
        filename_unsupported = "apidata/client_secrets/client_secret_unsupported.json"

        client_secret_bad_path = f"{self.BASE_PATH}/{filename_bad}"
        client_secret_unsupported_path = f"{self.BASE_PATH}/{filename_unsupported}"

        with pytest.raises(PyYouTubeException):
            Client(client_secret_path=client_secret_bad_path)

        with pytest.raises(PyYouTubeException):
            Client(client_secret_path=client_secret_unsupported_path)

    def test_request(self, key_cli):
        with pytest.raises(PyYouTubeException):
            cli = Client(client_id="id", client_secret="secret")
            cli.request(path="path", enforce_auth=True)

        with responses.RequestsMock() as m:
            m.add(method="GET", url="https://example.com", body="")
            key_cli.request(path="https://example.com")

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(method="GET", url=self.url, body=HTTPError("Exception"))
                key_cli.channels.list(channel_id="xxxxx")

    def test_parse_response(self, key_cli, helpers):
        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="GET",
                    url=self.url,
                    json=self.load_json("error_response.json", helpers),
                    status=400,
                )
                key_cli.channels.list(id="xxxx")

    def test_oauth(self, helpers):
        cli = Client(client_id="id", client_secret="secret")
        url, state = cli.get_authorize_url()
        assert state == "Python-YouTube"

        # test oauth flow
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=cli.EXCHANGE_ACCESS_TOKEN_URL,
                json=self.load_json("apidata/access_token.json", helpers),
            )
            token = cli.generate_access_token(code="code")
            assert token.access_token == "access_token"

            refresh_token = cli.refresh_access_token(refresh_token="token")
            assert refresh_token.access_token == "access_token"

        # test revoke access token
        with responses.RequestsMock() as m:
            m.add(
                method="POST",
                url=cli.REVOKE_TOKEN_URL,
            )
            assert cli.revoke_access_token(token="token")

        with pytest.raises(PyYouTubeException):
            with responses.RequestsMock() as m:
                m.add(
                    method="POST",
                    url=cli.REVOKE_TOKEN_URL,
                    json={"error": {"code": 400, "message": "error"}},
                    status=400,
                )
                cli.revoke_access_token(token="token")
