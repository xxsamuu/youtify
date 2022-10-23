import os
from threading import Timer
from urllib import response
import time

import google_auth_oauthlib.flow
import googleapiclient.discovery

from flask import redirect, jsonify

from dotenv import load_dotenv

import requests


load_dotenv()

class YoutubeStuff:
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "./YOUR_CLIENT_SECRET_FILE.json", "https://www.googleapis.com/auth/youtube.force-ssl")
    def __init__(self):
        #create a user when getting access to their account
        self.user = googleapiclient.discovery.build(
            "youtube", "v3", credentials=self.flow.run_local_server())
        self.url = self.flow.authorization_url()

    def createPlaylist(self, title, description, status, thumbnail=None):
        '''
        Automatically creates a playlist on users youtube, after getting permission via authorization pop-up.
        Default title should be the spotify playlist's one, but give possibility to change it manually
        '''
        status.get_status("creating playlist...")
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


        
    def add_tracks(self, playlist_id, tracks_names, status):
        status.get_status("kindly note that probable inefficency in matching the \ntracks might be due to APIs, and has nothing to do with the program itself.")
        time.sleep(2)
        video_data = []
        try:
            for i, track in enumerate(tracks_names):
                track_id= self.get_yt_id(track, status)
                if track_id:
                    status.get_status(f"adding {track} to playlist... ")
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
                    status.error_msg(f"cannot find the youtube video of {track}!", False)
                    continue
            status.get_status("")
            return video_data

        except:
            status.error_msg("cannot add tracks to playlist", True)
            self.delete_playlist(playlist_id)

    
    def delete_playlist(self, playlist_id):
        request = self.user.playlists().delete(
            id=playlist_id
        )
        
        request.execute()

        return 'playlist successfuly deleted'


    def get_yt_id(self, song_name, status):
        status.get_status(f"getting the youtube video of {song_name}...")
        API_KEY = os.getenv('YOUTUBE_API_KEY')
        link = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&q={song_name}&topicId=/m/04rlf&key={API_KEY}&maxResults=1"
        res = requests.get(link)
        data = res.json()
        if res.status_code == 200:
            items = data['items'][0]
            video_id = items['id']['videoId']
            return video_id
        else:
            return None

    def get_yt_playlists(self, status):
        if self.user:
            request = self.user.playlists().list(
                part="snippet, id",
                maxResults=50,
                mine=True
            )

            response = request.execute()

            playlists_data = []

            for i,playlist in enumerate(response["items"]):
                status.get_status(f"getting playlists...({round((i/ len(response['items'])) * 100)}%)")
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
        else:
            return self.url

    def getDefaultValues(self, playlist_id, item):
        if item != "thumbnail":
            if item == 'name':
                item = 'title'
            request = self.user.playlists().list(
                part="snippet",
                id=playlist_id
            )

            response = request.execute()
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

        
