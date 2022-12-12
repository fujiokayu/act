import requests
from bs4 import BeautifulSoup

import importlib.metadata

from act.config.toml_parser import config
from act.logging.logger import information_logger, error_logger

__version__ = importlib.metadata.version("act")


class User:
    def __init__(self, username: str, config_filepath: str):
        config_file = config(config_filepath, username)
        print(config_file)
        self.user_name = username
        self.auth_type = config_file.auth_type
        self.auth_param = config_file.auth_param
        self.auth_param_value = None
        self.endpoint_url = config_file.endpoint_url
        self.user_id = config_file.user_id
        self.password = config_file.password
        self.target_url = config_file.target_url
        self.session = requests.Session()

    @staticmethod
    def get_csrf_token(response):
        """Retrieve XSRF token.
        :param requests.Response response: response
        """
        return (
            BeautifulSoup(response.text, "html.parser")
            .find("input", attrs={"name": "authenticity_token"})
            .get("value")
        )

    @staticmethod
    def get_app_session(response):
        """Retrieve get_app_session token.
        :param requests.Response response: response
        """
        return (
            BeautifulSoup(response.text, "html.parser")
            .find("input", attrs={"name": "authenticity_token"})
            .get("value")
        )

    @staticmethod
    def get_user_agent():
        return {"user-agent": f"{__name__}/{__version__}"}

    def login(self):
        """Login to Authentication.endpoint_url
        title: Current Statistics
        :param str id: user_id
        :param str password: password
        """

        login_view_response = self.session.get(
            self.endpoint_url, headers=self.get_user_agent()
        )

        if login_view_response.status_code >= 400:
            error_logger(login_view_response)
            raise requests.exceptions.HTTPError(response=login_view_response)

        information_logger(login_view_response)

        login_post_response = self.session.post(
            self.endpoint_url,
            data="authenticity_token="
            + self.get_csrf_token(login_view_response)
            + "&user[email]="
            + self.user_id
            + "&user[password]="
            + self.password
            + "&user[remember_me]=0&commit=Log+in",
            headers=self.get_user_agent(),
        )
        if login_post_response.status_code >= 400:
            error_logger(login_post_response)
            print(login_post_response.text)
            raise requests.exceptions.HTTPError(response=login_post_response)

        self.auth_param_value = login_post_response.cookies.get(self.auth_param)
        information_logger(self.user_name + ": login succeed")

    def request_target(self):
        information_logger("request_target")
        target_response = self.session.get(
            self.target_url, headers=self.get_user_agent()
        )
        if target_response.status_code >= 400:
            error_logger(target_response)
            raise requests.exceptions.HTTPError(response=target_response)

        information_logger(target_response.text)
        print(target_response)
