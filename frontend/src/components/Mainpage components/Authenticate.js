import React, { useContext, useEffect, useState, useRef } from "react";
import { Context } from "../../Context";
import PlaylistWrapper from "./playlists handlers/PlaylistWrapper";

const Authenticate = ({ inputRef, seterror, error, setisLoading }) => {
  const { setmessage, originApp } = useContext(Context);
  const [playlistData, setplaylistData] = useState([]);
  const [spotifyData, setspotifyData] = useState();
  const [youtubeData, setyoutubeData] = useState();

  var intervalId;

  useEffect(() => {
    /*fetch user playlist on page load. */
    if (!error) {
      authenticationHandler();
    }
  }, [originApp]);

  useEffect(() => {
    /*
    to avoid forwarding requests to API each time page reloads, data are set in sessionStorage.
    If page reloads and there is no data, re-calls function to get playlist.
    */
    setplaylistData(JSON.parse(sessionStorage.getItem(`${originApp}Data`)));
    if (
      JSON.parse(sessionStorage.getItem(`${originApp}Data`) == null) &&
      !error
    ) {
      authenticationHandler();
      setplaylistData("");
    }
  }, []);

  async function getStatus() {
    fetch("https://youtify-api.onrender.com/api/get-status")
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setmessage(data.msg);
        seterror(data.error_data.error_msg);
      });
  }

  async function getPlaylists() {
    setisLoading(true);
    intervalId = setInterval(() => {
      getStatus();
    }, 1000);
    fetch(`https://youtify-api.onrender.com/api/getplaylists-${originApp}`)
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
  }

  const authenticationHandler = () => {
    if (originApp) {
      if (JSON.parse(sessionStorage.getItem(`${originApp}Data`)) == null) {
        getPlaylists();
      } else {
        setplaylistData(JSON.parse(sessionStorage.getItem(`${originApp}Data`)));
      }
    }
  };

  return (
    <div>
      {playlistData && (
        <PlaylistWrapper playlistData={playlistData} inputRef={inputRef} />
      )}
    </div>
  );
};

export default Authenticate;
