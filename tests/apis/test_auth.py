import json
import unittest

import responses
from requests import HTTPError

import pyyoutube


class TestOAuthApi(unittest.TestCase):
    BASE_PATH = "testdata/apidata/"

    with open(BASE_PATH + "access_token.json", "rb") as f:
        ACCESS_TOKEN_INFO = json.loads(f.read().decode("utf-8"))
    with open(BASE_PATH + "user_profile.json", "rb") as f:
        USER_PROFILE_INFO = json.loads(f.read().decode("utf-8"))

    def setUp(self) -> None:
        self.api = pyyoutube.Api(client_id="xx", client_secret="xx")

    def testInitApi(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            pyyoutube.Api()

    def testOAuth(self) -> None:
        url, statue = self.api.get_authorization_url()
        self.assertEqual(statue, "PyYouTube")

        redirect_response = (
            "https://localhost/?state=PyYouTube&code=code"
            "&scope=profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile#"
        )

        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.refresh_token()

        with responses.RequestsMock() as m:
            m.add(
                "POST", self.api.EXCHANGE_ACCESS_TOKEN_URL, json=self.ACCESS_TOKEN_INFO
            )
            token = self.api.generate_access_token(
                authorization_response=redirect_response,
            )
            self.assertEqual(token.access_token, "access_token")
            token_origin = self.api.generate_access_token(
                authorization_response=redirect_response, return_json=True
            )
            self.assertEqual(token_origin["access_token"], "access_token")

            refresh_token = self.api.refresh_token()
            self.assertEqual(refresh_token.access_token, "access_token")
            refresh_token_origin = self.api.refresh_token(return_json=True)
            self.assertEqual(refresh_token_origin["refresh_token"], "refresh_token")

            api = pyyoutube.Api(client_id="xx", client_secret="xx")
            refresh_token = api.refresh_token(refresh_token="refresh_token")
            self.assertEqual(refresh_token.refresh_token, "refresh_token")

    def testGetProfile(self) -> None:
        with self.assertRaises(pyyoutube.PyYouTubeException):
            self.api.get_profile()

        self.api._access_token = "access_token"
        with responses.RequestsMock() as m:
            m.add("GET", self.api.USER_INFO_URL, json=self.USER_PROFILE_INFO)
            profile = self.api.get_profile()
            self.assertEqual(profile.given_name, "kun")

            profile_origin = self.api.get_profile(return_json=True)
            self.assertEqual(profile_origin["given_name"], "kun")

        with responses.RequestsMock() as m:
            m.add("GET", self.api.USER_INFO_URL, body=HTTPError("Exception"))
            with self.assertRaises(pyyoutube.PyYouTubeException):
                self.api.get_profile()
