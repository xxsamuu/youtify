from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from youtube_stuff import YoutubeStuff

from spotify__stuff import SpotifyStuff

from get_status import GetStatus

from flask import Response


app = Flask('__name__', static_folder='./frontend/build', static_url_path='')
cors = CORS(app) 

status = GetStatus()

app.config['CORS_HEADERS'] = 'Content-Type'

youtube_user = ''
spotify_user = ''

@app.route('/api/hello', methods=['GET'])
@cross_origin()
def hello():
  return 'hello'

@app.route('/api/main',methods=['GET', 'POST'])
@cross_origin()
def main():
  """returns data about the playlist, such as: title, description, id.
  need playlist url passed in as paramater to the backend.
  need to add condition to check if playlist is converted from youtube to spotify or other way around. 
  """
  data  = request.get_json(force=True)
  origin_app = data['originApp']
  if origin_app == 'youtube':
    data['playlistLink'] = data['playlistLink'][38:]

  status.get_status("getting user's data...")
  user = ''

  if origin_app == 'spotify':
    global youtube_user
    if youtube_user == '':
      youtube_user = YoutubeStuff()
    user = youtube_user
  else:
    global spotify_user
    if spotify_user == '':
      spotify_user = SpotifyStuff()
    user = spotify_user

  return convert_handler(data, user)
  

def convert_handler(data, user):
  '''
  based on the user passed in (spotify/youtube) it creates and add 
  tracks to playlist. Returns informations about the playlist and the 
  tracks in it.
  '''
  global youtube_user
  tracks_name = []
  #for checking if items submitted are empty. If they are, search for the default ones.
  checked_data = getDefault(data)
  title = checked_data['name']
  description = checked_data['description']
  thumbnail = data['thumbnail']
  playlist = user.createPlaylist(title, description, status, thumbnail[23:])
  if data['originApp'] == 'spotify':
    tracks_name = SpotifyStuff.get_tracks_name(data['playlistLink'])
  else:
    tracks_name = youtube_user.get_tracks_name(data['playlistLink'])
  if playlist != None:
    add_tracks = user.add_tracks(playlist['id'], tracks_name, status)
    playlist['items'] = add_tracks
  return jsonify({
    "playlistData": playlist
  })


def getDefault(data):
  '''
  If user submit the form empty, this function will get its default
  values except for thumbnail, as in youtube it cannot be set.
  '''
  dataChecked = {}
  global youtube_user
  global spotify_user

  user = ''

  if data['originApp'] == 'spotify':
    user = spotify_user
  else:
    user = youtube_user
    
  for item in data:
    if not data[item]:
      status.get_status(f"getting the default value of {item}...")
      default = ''
      if data['originApp'] == 'spotify':
        default = SpotifyStuff.getDefaultValues(data['playlistLink'], item)
      else:
        default = youtube_user.getDefaultValues(data['playlistLink'], item)
      dataChecked[item] = default
    elif data[item]:
        dataChecked[item] = data[item]
  return dataChecked


@app.route('/api/check-validity', methods=['POST'])
@cross_origin()
def check_validity():
  """
  based on origin, it sends request to method to search for that playlist throughout its API,
  returning 200 if has matching result and 404 if not.
  """
  data = request.get_json(force=True)
  link = data['playlistLink']
  origin = data['originApp']
  val = ''
  if origin == 'spotify':
    spotify_user = SpotifyStuff()
    val = spotify_user.check_validity(link)
  else:
    global youtube_user
    if youtube_user == '':
      youtube_user = YoutubeStuff()
    val = youtube_user.check_validity(link)
  return Response(status=val)
  
    

@app.route('/api/get-status', methods=['GET', 'POST'])
@cross_origin()
def get_status():
  if status.fatal == True:
    pass
  return jsonify({
    "msg": status.msg,
    "error_data":{
      "error_msg": status.error,
      "is_fatal": status.fatal
    }
  })

@app.route('/api/getplaylists-spotify',methods=['GET','POST'])
@cross_origin()
def authenticate_spotify():
  status.get_status("getting user's data...")
  global spotify_user
  spotify_user = SpotifyStuff()
  data = spotify_user.get_users_playlists(status)
  return jsonify(data)

@app.route('/api/getplaylists-youtube', methods=['GET', 'POST'])
@cross_origin()
def authenticate_youtube():
  status.get_status("getting youtube playlists...")
  global youtube_user
  if youtube_user == '':
    youtube_user = YoutubeStuff()
  data = youtube_user.get_yt_playlists(status)
  return jsonify(data)

if __name__ == "__main__":
    app.run()
    # main()

