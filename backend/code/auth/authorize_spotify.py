import base64
from json import dump, load, loads, JSONDecodeError
from os import chmod, getenv
import os
from pathlib import Path
from typing import List

from requests import JSONDecodeError, request

from spotipy.oauth2 import SpotifyClientCredentials

import requests

import dotenv

import spotipy

from spotipy.exceptions import SpotifyException
from spotipy.oauth2 import SpotifyOauthError

from requests import HTTPError

dotenv.load_dotenv()

class Authorize:
    def __init__(
        self, 
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
        self.scope=scope
        self.token_file: Path = token_file
        self.session=None
        self.token=None
        self.client_id=getenv('SPOTIPY_CLIENT_ID')
        self.client_secret=getenv('SPOTIPY_CLIENT_SECRET')
        self.redirect_uri=redirect_uri
        self.auth_manager = SpotifyClientCredentials()

    def load_token(self):
        with open(self.token_file, 'r') as file:
            try:
                token = load(file)
            except:
                return None
        return token

    def save_token(self, token):
        with open(self.token_file, 'w') as file:
            dump(token, file)
        chmod(self.token_file, 0o600)

    def check_token_validity(self, token):
        try:
            spotipy.Spotify(auth=token, auth_manager=self.auth_manager)
            return 200
        except:
            return 401

    def get_new_token(self, auth_code):
        print('getting refresh token...')
        encoded = base64.b64encode((self.client_id + ":" + self.client_secret).encode("ascii")).decode()
        try:
            refresh_token = self.load_token()['refresh_token']
            print(refresh_token)
            req = request(
                method="POST", 
                url="https://accounts.spotify.com/api/token", 
                headers={
                    "Authorization": 'Basic ' + encoded ,
                    "Content-Type": "application/x-www-form-urlencoded"
                }, 
                data={
                    "refresh_token":refresh_token,
                    "grant_type":'refresh_token'
                }
            )      
            token = req.json()['access_token']  
            self.save_token(req.json())
            return token
        except:
            '''
            a "KeyError" is raised for the refresh_token variable;
            it means that token has been refreshed once and new token file doesnt contain 
            another refresh token. 
            Deletes text in json file and ask for another token with refresh token.
            '''
            with open(self.token_file, 'w') as f:
                f.truncate(0)
                self.new_session(auth_code)
        
    def new_session(self, auth_code):
        if auth_code:
            print('token not found, requesting one...')

            encoded = base64.b64encode((self.client_id + ":" + self.client_secret).encode("ascii")).decode()


            req = request(
                method="POST", 
                url="https://accounts.spotify.com/api/token", 
                headers={
                    "Authorization": 'Basic ' + encoded ,
                    "Content-Type": "application/x-www-form-urlencoded"
                }, 
                data={
                    "code":auth_code,
                    "redirect_uri":self.redirect_uri,
                    "grant_type":'authorization_code'
                }
            )

            token = ''

            self.save_token(req.json())

            try:
                token = req.json()['access_token']
            except:
                #if it raises am error. it means that access_token has expired.
                token = self.get_new_token(auth_code)

            service = spotipy.Spotify(auth=token, auth_manager=self.auth_manager)

            return service
        else:
            #user needs to re-authenticated
            print('auth_code not supplied.') 
            return 


    def authorize(self, auth_code): 
        load_token = self.load_token()
        token_is_valid = self.check_token_validity(load_token)
        try:
            if token_is_valid == 200:
                try:
                    print('token found!')
                    user = spotipy.Spotify(auth=token['access_token'], auth_manager=self.auth_manager)
                    return user
                except:
                    print('token expired')
                    token = self.get_new_token(auth_code)
                    user = spotipy.Spotify(auth=token, auth_manager=self.auth_manager)
                    return user     
        except (SpotifyOauthError, HTTPError):
            print('token expired, getting access token...')
            token = self.get_new_token()
            user = spotipy.Spotify(auth=token, auth_manager=self.auth_manager)
            return user
        
        else:
           self.new_session(auth_code)