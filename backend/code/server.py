from operator import imod
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from pyparsing import original_text_for
from youtube_stuff import YoutubeStuff

from spotify__stuff import SpotifyStuff

from get_status import GetStatus

from flask import Response


app = Flask(__name__)
app.secret_key = "usbdvsdkfvjskdfbvervrb34t'234tni34lfw4gub"

cors = CORS(app)

status = GetStatus()

app.config['CORS_HEADERS'] = 'Content-Type'

tries = 0


@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
  return 'homepage'

@app.route("/api/hello", methods=['GET', 'POST'])
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
    user = authentication_handler('youtube')
  else:
    user = authentication_handler('spotify')

  if user is not None:
    return convert_handler(data, user)
  else:
    return 'user not authenticated'


def authentication_handler(origin_app, auth_code):
  user = ''
  if origin_app == 'youtube':
    user =  YoutubeStuff(status, auth_code)
  else:
    user = SpotifyStuff(status)
  return user



def convert_handler(data, user):
  '''
  based on the user passed in (spotify/youtube) it creates and add
  tracks to playlist. Returns informations about the playlist and the
  tracks in it.
  '''
  tracks_name = []
  #for checking if params submitted in frontend form are empty (playlist name, playlist description...). If they are, search for the default ones.
  checked_data = getDefault(data)
  title = checked_data['name']
  description = checked_data['description']
  thumbnail = data['thumbnail']
  playlist = user.createPlaylist(title, description, status, thumbnail[23:])
  tracks_name = user.get_tracks_name(data['playlistLink'])
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

  user = authentication_handler(data['originApp'])

  for item in data:
    if not data[item]:
      status.get_status(f"getting the default value of {item}...")
      default = user.getDefaultValues(data['playlistLink'], item)
      dataChecked[item] = default
    elif data[item]:
        dataChecked[item] = data[item]
  return dataChecked


@app.route('/api/check-validity', methods=['POST'])
@cross_origin()
def check_validity():
  """
  takes as params from client-side link and originApp, and based on them it make a request to their APIs,
  returning 200 if playlist exists and 404 if not.
  """
  data = request.get_json(force=True)
  user = authentication_handler(data['originApp'])
  val = user.check_validity(data['playlistLink'])
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


@app.route('/api/getplaylists-<app_name>', methods=['GET', 'POST'])
@cross_origin()
def get_playlist(app_name):
  auth_code = ''
  if app_name == 'youtube':
    auth_code = request.args.get('code')
  print('inside backend function lev 1', auth_code)
  if not auth_code:
    #if frontend has not POST the auth_code, user has not guaranted access. User not authorized.
    return Response(status=401)
  else:
    user = authentication_handler(app_name, auth_code)
    playlists = user.get_playlists()
    return jsonify(playlists)
 


if __name__ == "__main__":
   app.run(host='0.0.0.0')

 