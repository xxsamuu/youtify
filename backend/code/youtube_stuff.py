import os
from threading import Timer
from urllib import response
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery

from flask import redirect, jsonify

from dotenv import load_dotenv

from auth.authorize_youtube import Authorize

import requests


load_dotenv()

authorize = Authorize(
    scope=['https://www.googleapis.com/auth/youtube.force-ssl'],
    token_file=r'C:\Users\samue\youtify\backend\code\tokens\token.json', 
    secrets_file=r'C:\Users\samue\youtify\backend\code\client_secret.json',
)

class YoutubeStuff:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    def __init__(self, status, auth_code):
        #create a user when getting access to their account
        self.status = status
        self.auth_code = auth_code
        self.user = authorize.authorize(auth_code=self.auth_code)
        

    def createPlaylist(self, title, description, thumbnail=None):
        '''
        Automatically creates a playlist on users youtube, after getting permission via authorization pop-up.
        Default title should be the spotify playlist's one, but give possibility to change it manually
        '''
        self.status.get_status("creating playlist...")
        makeRequest = self.user.playlists().insert(
            part="snippet,status, id",
            body={
            "snippet": {
                "title": title,
                "description": description,
                "defaultLanguage": "en",
            },
            "status": {
                "privacyStatus": "private"
            }
            }
        )
        response = makeRequest.execute()

        return {
            "playlistName": response['snippet']['title'],
            "playlsitDescription": response['snippet']['description'],
            "id": response['id']
        }
        
    def get_tracks_name(self, id):
        array_names = []
        request = self.user.playlistItems().list(
            part="snippet",
            playlistId=id,
            maxResults=50
        )
        response = request.execute()
        for track in response["items"]:
            array_names.append(track["snippet"]["title"])
        
        return array_names


        
    def add_tracks(self, playlist_id, tracks_name ):
        print(tracks_name)
        self.status.get_status("kindly note that probable inefficency in matching the \ntracks might be due to APIs, and has nothing to do with the program itself.")
        time.sleep(2)
        video_data = []
        for track in tracks_name:
            track_id= self.get_yt_id(track)
            print(track, track_id)
            if track_id:
                self.status.get_status(f"adding {track} to playlist... ")
                request = self.user.playlistItems().insert(
                    part="snippet",
                    body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                        "kind": "youtube#video",
                        "videoId": track_id
                        }
                        },
                    },
                )
                response = request.execute()

                videos_title = response['snippet']['title']
                videos_id = response['id']

                video_data.append({
                    "videoTitle": videos_title,
                    "videoId": videos_id
                })
            else:
                print('couldnt find the video of ', track)
                self.status.error_msg(f"cannot find the youtube video of {track}!", False)
                continue
            self.status.get_status("")
        return video_data

    def get_yt_id(self, song_name):
        request = self.user.search().list(
            part='snippet',
            maxResults=1,
            q=song_name,
            topicId="10"
        )
        response = request.execute()
        self.status.get_status(f"getting the youtube video of {song_name}...")
        try:
            id = response['items'][0]["id"]["videoId"]
            return id
        except:
            return None

    def delete_playlist(self, playlist_id):
        request = self.user.playlists().delete(
            id=playlist_id
        )
        
        request.execute()

        return 'playlist successfuly deleted'


    def get_playlists(self):
        if not self.user:
            self.status.get_status('please visit this url to grant us access: {}'.format(self.authorize.get_auth_link()))
        request = self.user.playlists().list(
            part="snippet, id",
            maxResults=50,
            mine=True
        )

        response = request.execute()

        playlists_data = []

        for i,playlist in enumerate(response["items"]):
            self.status.get_status(f"getting playlists...({round((i/ len(response['items'])) * 100)}%)")
            data = {
                "playlist_name": playlist["snippet"]["title"],
                "playlist_url": f"https://www.youtube.com/playlist?list={playlist['id']}",
                "id": playlist["id"],
                "image": playlist["snippet"]["thumbnails"]["default"]["url"]
            }
            if data["image"] == '[]':
                pass
            else:
                playlists_data.append(data)

        return playlists_data

    def getDefaultValues(self, playlist_id, item):
        if item != "thumbnail":
            if item == 'name':
                item = 'title'
            request = self.user.playlists().list(
                part="snippet",
                id=playlist_id
            )
            print(playlist_id, item)
            response = request.execute()
            print(response)
            return response["items"][0]["snippet"][item]
        else:
            return None

    def check_validity(self, link):
        request = self.user.playlists().list(
            part='snippet',
            id=link[38:]
        )
        response = request.execute()
        if len(response["items"]):
            return 200
        else:
            return 404

    