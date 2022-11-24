import base64
from json import dump, load
from os import chmod, getenv
from pathlib import Path
from typing import List

import json

from requests import JSONDecodeError, request

import requests

import dotenv

import spotipy

dotenv.load_dotenv()

class Authorize:
    def __init__(
        self, 
        auth_code, 
        scope: List[str], 
        token_file: Path,
        redirect_uri
    ):
        """
        This class handles the interaction between the client-side request to Spotify API
        and the Spotipy library and its methods.
        Args:
            auth_code: the code that the frontend gets when user accepts access.
            For more info: https://developer.spotify.com/documentation/general/guides/authorization/code-flow/
            scope: list of the permissions that the application needs.
            token_file: full path of the file in which access token and refresh token will be stored.
            redirect_uri:the registered redirect_uri. Must match the one in Spotify Dashboard.
        """
        self.auth_code = auth_code
        self.scope=scope
        self.token_file: Path = token_file
        self.session=None
        self.token=None
        self.client_id=getenv('SPOTIPY_CLIENT_ID')
        self.client_secret=getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri=redirect_uri

    def load_token(self):
        try:
            with open(self.token_file, 'r') as file:
                token = load(file)
        except (JSONDecodeError, IOError):
            return None
        return token

    def save_token(self, token):
        with open(self.token_file, 'w') as file:
            dump(token, file)
        chmod(self.token_file, 0o600)

    def authorize(self):
        token = self.load_token

        if token:
            print('spotify token found, starting session...')
            user = spotipy.Spotify(auth=token)
            return user
        
        else:
            print('token not found, requesting one...')
            requests.post
            req = request(
                method="POST", 
                url="https://accounts.spotify.com/api/token", 
                headers={'Authorization': 'Basic' + f"{base64.encode(self.client_id)}:{base64.encode(self.client_secret)}"}, 
                json={
                    "code":self.auth_code,
                    "redirect_uri":self.redirect_uri,
                    "grant_type":'authorization_code'
                }
            )
            print(req.status_code)
            if req.status_code == 200:
                print(f">>>Success!! token: {json.loads(req.json())['access_token'] }")
            else:
                print(f"error!")