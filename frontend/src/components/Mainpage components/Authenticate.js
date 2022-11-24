import React, { useContext, useEffect, useState, useCallback } from "react";
import { Context } from "../../Context";
import PlaylistWrapper from "./playlists handlers/PlaylistWrapper";
import GoogleButton from "react-google-button";
import { gapi } from "gapi-script";
const Authenticate = ({ inputRef, seterror, error, setisLoading }) => {
  /*
  Since this is the first time the web-app asks for user permission, the oauth is implemented here. 
  Oauth2 flow: first, redirect the user to oauth consent page to guarantee access to their data, 
  then get the auth_code and POST it to the backend, which fully handles the build of the service,
  and then request to access their playlist and list them.
  */
  const { setmessage, originApp } = useContext(Context);
  const [isAuthenticated, setisAuthenticated] = useState(false);
  const [playlistData, setplaylistData] = useState([]);
  const [user, setuser] = useState();
  const [spotifyData, setspotifyData] = useState();
  const [youtubeData, setyoutubeData] = useState();

  const client_id =
    "197724356935-fro7lihg5rs2lhf98g7k9vdgk2mi7lar.apps.googleusercontent.com";

  const scope = "https://www.googleapis.com/auth/youtube.force-ssl";
  var intervalId;

  useEffect(() => {
    /*fetch user playlist on page load. 
    if (isAuthenticated) {
      getPlaylistsfromStorage();
    }
    */
  }, []);

  const clickHandler = () => {
    getPlaylistsfromStorage();
  };

  async function getStatus() {
    fetch("/api/get-status")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setmessage(data.msg);
        seterror(data.error_data.error_msg);
      });
  }

  const handleAuthentication = () => {
    let auth_code = "";
    if (originApp === "youtube") {
      getYtCode();
    }

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

  const getYtCode = useCallback(() => {
    console.log("entered getYtCode() function");
    const googleAuthUrl = "https://accounts.google.com/o/oauth2/v2/auth";
    const redirectUri = "http://localhost:5000/api/getplaylists-youtube";
    const params = {
      response_type: "code",
      client_id: client_id,
      redirect_uri: redirectUri,
      prompt: "select_account",
      access_type: "offline",
      scope,
    };
    const urlParams = new URLSearchParams(params).toString();
    console.log("oauth url: ", googleAuthUrl, "?", urlParams);
    window.location = `${googleAuthUrl}?${urlParams}`;
  }, []);

  const getSpCode = () => {};

  async function playlistsHandler() {
    if (!isAuthenticated) {
      handleAuthentication();
    }
    setisLoading(true);

    intervalId = setInterval(() => {
      if (!error) {
        getStatus();
      }
    }, 1000);

    fetchPlaylists(intervalId);
  }

  const fetchPlaylists = (intervalId) => {
    fetch(`/api/getplaylists-${originApp}`)
      .then((res) => res.json())
      .then((data) => {
        clearInterval(intervalId);
        setisLoading(false);
        originApp === "spotify" ? setspotifyData(data) : setyoutubeData(data);
        sessionStorage.setItem(`${originApp}Data`, JSON.stringify(data));
      })
      .catch((error) => {
        seterror(
          "error while trying to connect to the server. \nRefresh the page and try again."
        );
        setisLoading(false);
        clearInterval(intervalId);
      });
  };

  const getPlaylistsfromStorage = () => {
    if (originApp) {
      if (JSON.parse(sessionStorage.getItem(`${originApp}Data`)) == null) {
        playlistsHandler();
      } else {
        setplaylistData(JSON.parse(sessionStorage.getItem(`${originApp}Data`)));
      }
    }
  };

  return (
    <div>
      <GoogleButton onClick={getYtCode} label="Sign in with Google" />
      {playlistData && (
        <PlaylistWrapper playlistData={playlistData} inputRef={inputRef} />
      )}
    </div>
  );
};

export default Authenticate;
