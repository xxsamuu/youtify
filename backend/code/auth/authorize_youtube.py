import logging
from json import JSONDecodeError, dump, load
from os import chmod
from pathlib import Path
from typing import List, Optional
import googleapiclient.discovery
import requests_oauthlib
import httplib2
import google.oauth2.credentials

from oauth2client import client

from google_auth_oauthlib.flow import InstalledAppFlow
from requests import request
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from urllib3.util.retry import Retry

import requests

import get_status

log = logging.getLogger(__name__)


# OAuth endpoints given in the Google API documentation
authorization_base_url = "https://accounts.google.com/o/oauth2/v2/auth"
token_uri = "https://www.googleapis.com/oauth2/v4/token"

status = get_status.GetStatus()


class Authorize:
    def __init__(
        self,
        scope: List[str],
        token_file: Path,
        secrets_file: Path,
        max_retries: int = 5,
        port: int = 8080,
    ):
        """A very simple class to handle Google API authorization flow
        for the requests library. Includes saving the token and automatic
        token refresh.
        Args:
            scope: list of the scopes for which permission will be granted
            token_file: full path of a file in which the user token will be
            placed. After first use the previous token will also be read in from
            this file
            secrets_file: full path of the client secrets file obtained from
            Google Api Console
        """
        self.max_retries = max_retries
        self.scope: List[str] = scope
        self.token_file: Path = token_file
        self.session = None
        self.token = None
        self.secrets_file = secrets_file
        self.port = port
        self.auth_link = ''

        try:
            with open(secrets_file, 'r') as stream:
                all_json = load(stream)
            secrets = all_json["web"]
            self.client_id = secrets["client_id"]
            self.client_secret = secrets["client_secret"]
            self.redirect_uri = secrets["redirect_uris"][0]
            self.token_uri = secrets['token_uri']
            self.extra = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            }

        except (JSONDecodeError, IOError):
            print("missing or bad secrets file: {}".format(secrets_file))
            exit(1)

    def load_token(self) -> Optional[str]:
        try:
            with open(self.token_file, 'r') as stream:
                token = load(stream)
        except (JSONDecodeError, IOError):
            return None
        return token

    def save_token(self, token: str):
        with open(self.token_file, 'w') as stream:
            dump(token, stream)
        chmod(self.token_file,0o600 )

    def store_users(self, credentials):
        '''
        this method allow me to hold a record of users who accessed my service.
        Stored in a text file.
        '''
        authenticated_user = googleapiclient.discovery.build('oauth2', 'v2', credentials=credentials)
        authenticated_user_info = authenticated_user.userinfo().get().execute()
        with open('users.txt', 'w') as file:
            file.write(authenticated_user_info['email'])

    def authorize(self, auth_code):
        """Initiates OAuth2 authentication and authorization flow"""
        token = self.load_token()

        if token:
            print('token found. Starting Session...')
            #ft_token = requests_oauthlib.OAuth2Session.fetch_token()
            credentials = google.oauth2.credentials.Credentials(
                token['access_token'],
                refresh_token=token['refresh_token'],
                token_uri=self.token_uri, #
                client_id=self.client_id, #
                client_secret = self.client_secret, #
                scopes = self.token_uri
            )
            service = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
        
            return service
            '''self.session = OAuth2Session(
                self.client_id,
                token=token,
                auto_refresh_url=self.token_uri,
                auto_refresh_kwargs=self.extra,
                token_updater=self.save_token,
            )'''
        else:
            data = {
                'code': auth_code,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'redirect_uri': self.redirect_uri,
                'grant_type': 'authorization_code',
                'scopes': self.scope
            }
            res = requests.post('https://oauth2.googleapis.com/token', data=data).json()

            oauth2_token = {
                "access_token": res['access_token'],
                "refresh_token": res['refresh_token'],
                "token_type": "Bearer",
                "scope": res['scope'],
                "expires_at": res['expires_in'],
            }

            credentials = google.oauth2.credentials.Credentials(
                res['access_token'],
                refresh_token=res['refresh_token'],
                token_uri=self.token_uri, #
                client_id=self.client_id, #
                client_secret = self.client_secret, #
                scopes =self.token_uri
            )

            self.save_token(oauth2_token)

            service = googleapiclient.discovery.build('youtube', 'v3', credentials=credentials)
            
            return service

        # set up the retry behaviour for the authorized session
        retries = Retry(
            total=self.max_retries,
            backoff_factor=5,
            status_forcelist=[500, 502, 503, 504, 429],
            allowed_methods=frozenset(["GET", "POST"]),
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        # apply the retry behaviour to our session by replacing the default HTTPAdapter
        self.session.mount("https://", HTTPAdapter(max_retries=retries))