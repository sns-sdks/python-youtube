"""
    Tests for client.
"""
import pytest

import responses
from requests import HTTPError

from .base import BaseTestCase
from pyyoutube import Client, PyYouTubeException


class TestClient(BaseTestCase):
    base_path = "testdata"
    resource = "channels"

    def test_initial(self):
        with pytest.raises(PyYouTubeException):
            Client()

        cli = Client(api_key="key", headers={"HA": "P"})
        assert cli.session.headers["HA"] == "P"

    def test_has_client_id_and_secret(self):
        assert Client(api_key="key").has_client_id_and_secret() is False
        client = Client(api_key="key", client_id="client", client_secret="secret")
        assert client.has_client_id_and_secret() is True

    def test_has_api_key(self):
        assert Client().has_api_key() is False
        assert Client(api_key="key").has_api_key() is True

    def test_has_access_token(self):
        assert Client(api_key="key").has_access_token() is False
        assert Client(access_token="access-token").has_access_token() is True

    def test_convert_json_to_dict(self):
        result = Client.convert_json_to_dict({"test": "test"})
        assert result == {"test": "test"}

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
