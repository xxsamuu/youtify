import json
import math
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

import spotipy.util as util

from dotenv import load_dotenv


from get_status import GetStatus


load_dotenv()

        
class SpotifyStuff:
    try:
        os.environ['SPOTIPY_CLIENT_ID'] = os.getenv('SPOTIPY_CLIENT_ID')
        os.environ['SPOTIPY_CLIENT_SECRET'] = os.getenv('SPOTIPY_CLIENT_SECRET')
    except:
        pass
    scope=['playlist-modify-public', 'playlist-modify-private', 'playlist-read-private', 'ugc-image-upload']
    
    auth = SpotifyOAuth(
        redirect_uri='http://localhost:3000/callback', 
        scope=scope,
    )


    def __init__(self):
        #create a user when getting access to their account
        self.user = spotipy.Spotify(auth_manager=self.auth)


    def get_users_playlists(self, status):
        playlists = self.user.current_user_playlists(50)
        data = []
        for i, playlist in enumerate(playlists['items']):
            status.get_status(f"getting playlists...({round((i / len(playlists['items'])) * 100)}%)")
            playlist_id = playlist['id']
            playlist_data = {
                "playlist_name": playlist['name'],
                "playlist_url": playlist['external_urls']['spotify'],
                "id": playlist_id,
                "image": self.user.playlist_cover_image(playlist_id)
            }
            if len(playlist_data['image']) == 0:
                #if playlist has no image, it's empty.
                continue
            else:
                data.append(playlist_data)
        status.get_status("")
        return data

    def createPlaylist(self, title, description,status,  thumbnail  ):
        status.get_status("creating spotify playlist...")
        try:
            playlist = self.user.user_playlist_create(self.user.me()['id'], title, public=False, collaborative=False, description=description)

            if len(thumbnail):
                status.get_status("uploading image as cover...")
                try:
                    self.user.playlist_upload_cover_image(playlist['id'], thumbnail)
                except:
                    status.error_msg("invalid image selected, setting the default one...", False)

            return {
                "playlistName": playlist['name'],
                "playlistDescription": playlist["description"],
                "id": playlist["id"],
                "coverImage": playlist["images"]
            }
        except:
            status.error_msg('error trying to create the playlist.\nTry again.', True)
            return None
    

    def add_tracks(self, playlist_id, tracks_name, status):
        status.get_status("kindly note that probable inefficency in matching the \ntracks might be due to APIs, and has nothing to do with the program itself.")
        time.sleep(2)
        tracks_data = []
        not_songs = 0
        try:
            for i,track in enumerate(tracks_name):
                track_id = self.get_sp_id(track)
                if track_id:
                    status.get_status(f"adding {track} to playlist... ")
                    self.user.playlist_add_items(playlist_id, track_id)
                    tracks_data.append({
                        "songName": track
                    })
                else:
                    not_songs += 1
                    status.error_msg(f'{track} is not a song!', False)
            
            if not_songs + 1 == len(tracks_name) :
                status.error_msg(f'Warning: playlist does not contain any song. \n Try again.', True)
                self.delete_playlist(playlist_id)
                raise "playlist does not contain any song."

            else:
                return tracks_data
        except:
            status.error_msg(f'An error occured while trying to add tracks to playlist.', True)
            self.delete_playlist(playlist_id)


    def delete_playlist(self, playlist_id):
        self.user.current_user_unfollow_playlist(playlist_id)
        return 'playlist deleted'



    def get_sp_id(self, track ):
        res = self.user.search(q=track,limit=1, type="track")

        if res["tracks"]["items"] == "[]":
            return None
        else:
            id = res["tracks"]["items"][0]["id"]
            return [id]

    def check_validity(self, link):
        try:
            self.user.playlist(link)
            return 200
        except:
            return 404

    @classmethod
    def get_tracks_name(cls, link):
        credentials = SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=credentials)
        array_data = sp.playlist_tracks(link)['items']
        array_names = []
        for track in array_data:
            array_names.append(track['track']['name'])
        return array_names


    @classmethod
    def getDefaultValues(cls, link, item):
        credentials = spotipy.SpotifyClientCredentials()
        sp = spotipy.Spotify(auth_manager=credentials)

        if item != "thumbnail":
            default =  sp.playlist(link)[item]
            return default
        else:
            #if item searched for is the thumbnail. Thumbnail in youtube playlists
            #cannot be modified.
            return None


            
    def useless_method(self):
        return "some useless method just for testing."
