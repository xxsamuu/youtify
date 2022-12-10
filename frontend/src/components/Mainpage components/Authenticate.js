import React, { useContext, useEffect, useState, useCallback } from "react";
import { Context } from "../../Context";
import PlaylistWrapper from "./playlists handlers/PlaylistWrapper";
import GoogleButton from "react-google-button";
import { useNavigate } from "react-router-dom";
import SpotifyLogin from "react-spotify-login";
import spotify from "../../images/spotify.png";
const Authenticate = ({ inputRef, seterror, error, setisLoading }) => {
  /*
  Since this is the first time the web-app asks for user permission, the oauth is implemented here. 
  Oauth2 flow: first, redirect the user to oauth consent page to guarantee access to their data, 
  then get the auth_code and POST it to the backend, which fully handles the build of the service,
  and then request to access their playlist and list them.
  */
  const { setmessage, originApp, setOriginApp } = useContext(Context);
  const [isAuthenticated, setisAuthenticated] = useState(false);
  const [getStatusInterval, setgetStatusInterval] = useState();
  const [playlistData, setplaylistData] = useState([]);
  const [user, setuser] = useState();
  const [spotifyData, setspotifyData] = useState([]);
  const [youtubeData, setyoutubeData] = useState([]);
  const [statusCode, setstatusCode] = useState();

  const client_id =
    "197724356935-fro7lihg5rs2lhf98g7k9vdgk2mi7lar.apps.googleusercontent.com";

  const scope = "https://www.googleapis.com/auth/youtube.force-ssl";

  let navigate = useNavigate();

  useEffect(() => {
    console.log(originApp);
    setplaylistData("");
    getPlaylistsfromStorage();
  }, [originApp]);

  useEffect(() => {
    isAuthenticated
      ? getPlaylistsfromStorage()
      : console.log("user not authenticated");
  }, [isAuthenticated]);

  useEffect(() => {
    clearInterval(getStatusInterval);
  }, [playlistData]);

  const handleAuthentication = () => {
    let auth_code = "";

    /*originApp === "spotify" ? (auth_code = getSpCode) : (auth_code = getYtCode);
    fetch(`/api/getplaylists-${originApp}`, {
      method: "POST",
      body: JSON.stringify({ auth_code }),
    }).then((res) => {
      if (res.status === 401) {
        seterror("user denied access.");
        return;
      } else {
        setisAuthenticated(true);
        playlistsHandler();
      }
    });*/
  };

  const googleClickHandler = () => {
    let get_code = getYtCode();
    if (get_code === "done") {
      console.log("exited getYtCode fn");
      getStatusLogin();
    }
  };

  const spotifyClickHandler = () => {
    let get_code = getSpCode();
    if (get_code === "done") {
      console.log("exited getSpCode fn");
      getStatusLogin();
    }
  };

  const getYtCode = useCallback(() => {
    console.log("entered getYtCode() function");
    const googleAuthUrl = "https://accounts.google.com/o/oauth2/v2/auth";
    const params = {
      response_type: "code",
      client_id: client_id,
      redirect_uri: "http://localhost:5000/api/login-youtube",
      prompt: "select_account",
      access_type: "offline",
      scope,
    };
    const urlParams = new URLSearchParams(params).toString();
    window.open(`${googleAuthUrl}?${urlParams}`);
    return "done";
  }, []);

  const getSpCode = useCallback(() => {
    console.log("entered getSpCode() function");
    const spotifyAuthUrl = "https://accounts.spotify.com/authorize";
    const redirectUri = "http://localhost:5000/api/login-spotify";
    const params = {
      response_type: "code",
      client_id: "f823a25983b3432baa175ff6b3de292a",
      scope:
        "playlist-modify-public playlist-modify-private playlist-read-private ugc-image-upload user-read-email",

      redirect_uri: redirectUri,
    };
    const urlParams = new URLSearchParams(params).toString();
    window.open(`${spotifyAuthUrl}?${urlParams}`);
    return "done";
  }, []);

  const getStatusLogin = () => {
    let interval = setInterval(() => {
      setstatusCode("");
      fetch("/api/login-status")
        .then((res) => res.json())
        .then((data) => {
          console.log(data);
          setstatusCode(data.status_code);
          if (data.status_code === 200) {
            setisAuthenticated(true);
            clearInterval(interval);
            JSON.stringify(sessionStorage.setItem("isLoggedIn", true));
          } else if (
            statusCode !== 200 ||
            statusCode !== undefined ||
            data.status_code === null
          ) {
            console.log(data.status_code);
            seterror(
              `had an error while trying to log user. Error code: ${statusCode}`
            );
          }
        })
        .catch((error) => console.log(error));
    }, 1000);
    if (isAuthenticated == true) {
      getPlaylistsfromStorage();
    }
  };

  async function getStatus() {
    fetch("/api/get-status")
      .then((res) => res.json())
      .then((data) => {
        setmessage(data.msg);
        seterror(data.error_data.error_msg);
      });
  }

  async function playlistsHandler() {
    console.log("playlisthandler fn");
    if (!isAuthenticated) {
      console.log("not authenticated");
      return;
    }

    setisLoading(true);

    fetchPlaylists();

    let interval = setInterval(() => {
      getStatus();
    }, 1000);

    setgetStatusInterval(interval);
  }

  const fetchPlaylists = () => {
    console.log("inside fetchplaylist fn");
    fetch(`/api/getplaylists-${originApp}`)
      .then((res) => res.json())
      .then((data) => {
        setisLoading(false);
        originApp == "youtube"
          ? setyoutubeData([...youtubeData, { ...data }])
          : setspotifyData([...spotifyData, { ...data }]);
        sessionStorage.setItem(`${originApp}Data`, JSON.stringify(data));
      })
      .catch((error) => {
        seterror(
          "error while trying to connect to the server. \nRefresh the page and try again."
        );
        setisLoading(false);
      });
  };

  const getPlaylistsfromStorage = () => {
    if (JSON.parse(sessionStorage.getItem(`${originApp}Data`)) == null) {
      playlistsHandler();
    } else {
      setplaylistData(JSON.parse(sessionStorage.getItem(`${originApp}Data`)));
    }
  };

  return (
    <div>
      {playlistData == 0 ? (
        originApp === "youtube" ? (
          <GoogleButton
            onClick={googleClickHandler}
            label="Sign in with Google"
          />
        ) : (
          <button className="spotifyButtonLogin" onClick={spotifyClickHandler}>
            <img src={spotify} />
          </button>
        )
      ) : (
        <PlaylistWrapper playlistData={playlistData} inputRef={inputRef} />
      )}
    </div>
  );
};

export default Authenticate;
