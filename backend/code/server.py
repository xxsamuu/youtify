from operator import imod
from flask import Flask, jsonify, request, session
from flask_cors import CORS, cross_origin
from pyparsing import original_text_for
from youtube_stuff import YoutubeStuff

from spotify__stuff import SpotifyStuff

from get_status import GetStatus

from flask import Response, redirect

import flask

yt_user = ''
sp_user = ''

allowed_origin_apps = ['spotify', 'youtube']

p = [
  {
  'user': yt_user,
  'originApp': 'youtube',
  'class': YoutubeStuff
  },
  {
    'user': sp_user,
    'originApp': 'spotify',
    'class': SpotifyStuff
  }  
]

auth_code = ''

app = Flask(__name__)
app.secret_key = "usbdvsdkfvjskdfbvervrb34t'234tni34lfw4gub"

cors = CORS(app)

status = GetStatus()
login_status = GetStatus()

app.config['CORS_HEADERS'] = 'Content-Type'

tries = 0


@app.route('/', methods=['GET'])
@cross_origin()
def homepage():
  return 'homepage'


@app.route('/api/main',methods=['GET', 'POST'])
@cross_origin()
def main():
  """
  returns data about the playlist, such as: title, description, id.
  need playlist url passed in as paramater to the backend.
  """
  data  = request.get_json()
  print(data)
  origin_app = data['originApp']

  status.get_status("getting user's data...")
  user = ''

  if origin_app == 'spotify':
    user = authentication_handler('youtube', '')
  else:
    user = authentication_handler('spotify', '')

  if user is not None:
    return convert_handler(data, user)
  else:
    return Response('user not authenticated', status=401)


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
  playlist = user.createPlaylist(title, description, thumbnail[23:])
  other_user = ''
  if data['originApp'] == 'spotify':
    global sp_user
    other_user = sp_user
  else:
    global yt_user
    other_user = yt_user
  print(f"user: {user}; other user: {other_user}")
  tracks_name = other_user.get_tracks_name(data['playlistLink'])
  if playlist != None:
    add_tracks = user.add_tracks(playlist['id'], tracks_name)
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

  user = authentication_handler(data['originApp'], '')

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
  checks if url posted from client is an actual playlist or not
  """
  data = request.get_json(force=True)
  user = authentication_handler(data['originApp'], '')
  val = user.check_validity(data['playlistLink'])
  return Response(status=val)


@app.route('/api/get-status', methods=['GET'])
@cross_origin()
def get_status():
  return jsonify({
    "msg": status.msg,
    "error_data":{
      "error_msg": status.error,
      "is_fatal": status.fatal,
    },
    "code": status.status_code
  })


def authentication_handler(origin_app, auth_code):
  '''
  check if the given originapp has an initialized object or not;
  if not, initialize one with the given auth_code.
  If auth_code is not passed in and flask server is trying to reach app-server endpoints, 
  user need to login again.
  '''
  global yt_user
  global sp_user
  if origin_app == 'youtube':
    if yt_user == '':
      print('initializing youtube user...')
      yt_user = YoutubeStuff(status, auth_code=auth_code)
    return yt_user
  else:
    if sp_user == '':
      print('initializing spotify user...')
      sp_user = SpotifyStuff(status, auth_code=auth_code)
    return sp_user



@app.route('/api/login-status', methods=['GET'])
@cross_origin()
def return_status():
  return jsonify({
    "data": login_status.msg,
    "status_code": login_status.status_code
  })


def clear_previous_state(obj):
  obj.clear()
  return obj

@app.route('/api/login-<app_name>', methods=['GET', 'POST'])
@cross_origin()
def login(app_name):
  code = ''
  state = clear_previous_state(login_status)
  p = ['code', 'access_token']
  if app_name.lower() not in allowed_origin_apps or app_name == '':
    state.login_status('invalid URL bro', status_code=404)

  if not [request.args.get(x) for x in p]:
    #if frontend has not POST the auth_code, return bad request error
    state.login_status('need to POST auth_code first', status_code=401)
  else:
    code = request.args.get('code')
    authentication_handler(app_name, code)
    state.login_status('user successfully logged in', status_code=200)
      
  return jsonify({
    "data": state.msg,
    "status_code": state.status_code
  })

@app.route('/api/getplaylists-<app_name>', methods=['GET', 'POST'])
@cross_origin()
def get_playlist(app_name):
  user = ''
  if app_name.lower() not in allowed_origin_apps:
    return Response('Invalid URL bro', status=404)
  else:
    try:
      if app_name == 'youtube':
        global yt_user
        playlists = yt_user.get_playlists()
      else:
        global sp_user
        playlists = sp_user.get_playlists()

      return jsonify(playlists)
    except:
      status.error_msg('sorry about that. You may need to retry.', True)
      return Response('sorry about that. You may need to retry.', 500)


if __name__ == "__main__":
   app.run(host='0.0.0.0')

 