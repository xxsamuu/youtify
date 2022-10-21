import React, { useContext, useEffect, useRef, useState } from "react";
import Configure from "./Configure";
import Authenticate from "./Mainpage components/Authenticate";
import { Context } from "../Context";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
//import "font-awesome/css/font-awesome.min.css";
import { faSpotify } from "@fortawesome/free-brands-svg-icons";
const Mainpage = ({ setsuccess, seterror, error, setisLoading, isLoading }) => {
  const {
    title,
    setTitle,
    originApp,
    setOriginApp,
    setplaylistLink,
    playlistLink,
    isFromPlaylist,
  } = useContext(Context);
  const inputRef = useRef();
  //indicate what app should the programm retrieve the playlists from
  const [configure, setconfigure] = useState(false);
  const [opacity, setOpacity] = useState({ opacity: 1 });

  const configurePlaylist = (e) => {
    /* 
    check if link submitted is from user playlist or input
    */
    e.preventDefault();
    if (!title) {
      setTitle("");
      setconfigure(true);
    } else {
      urlFromUser();
    }
  };

  const urlFromUser = () => {
    if (title.length < 72) {
      seterror(
        "invalid playlist link. Either enter a spotify playlist link or a youtube one."
      );
      setTitle("");
    } else if (title.length == 76 || title.length == 112) {
      checkLinkValidity(title, "spotify");
    } else if (title.length == 72) {
      checkLinkValidity(title, "youtube");
    }
  };

  const checkLinkValidity = (playlistLink, originApp) => {
    /*
    check the validity of a users submitted link by posting it to backend source, which takes the link
    and forward a request to its originApp API (Youtube, Spotify) and see if it exist.
    Returns status 200 if success and 404 for not found.
    */
    setOriginApp(originApp);
    fetch("https://youtify-api.onrender.com/api/check-validity", {
      method: "POST",
      body: JSON.stringify({ playlistLink, originApp }),
    }).then((res) => {
      if (res.status == 200) {
        setplaylistLink(playlistLink);
        setconfigure(true);
        setTitle("");
        return true;
      } else if (res.status === 404) {
        seterror("not a valid link.");
        return false;
      } else {
        seterror("error trying to connect to the server.");
      }
    });
  };

  useEffect(() => {
    setOpacity(!configure ? { opacity: "1" } : { opacity: 0.5 });
  }, [configure]);

  const clickHandler = () => {
    /* 
    to close configure prompt when user clicks on page.
    */
    if (configure) {
      setconfigure(false);
    }
  };

  return (
    <div className="mainpage">
      <div className="mainpage-wrapper" onClick={clickHandler} style={opacity}>
        <div className="options" style={{ display: "flex" }}>
          <label className="originApp">
            From
            {originApp == "spotify" ? (
              <i className="fa fa-spotify"></i>
            ) : (
              <i className="fa fa-youtube"></i>
            )}
            <select
              className="option"
              onChange={(e) => setOriginApp(e.target.value)}
            >
              <option value="spotify">spotify</option>
              <option value="youtube">youtube</option>
            </select>
          </label>
          <label className="toApp" style={{ display: "flex" }}>
            to
            {originApp == "spotify" ? (
              <i className="fa fa-youtube"></i>
            ) : (
              <i className="fa fa-spotify"></i>
            )}
            <select onChange={(e) => setOriginApp(e.target.value)}>
              <option value={originApp == "spotify" ? "youtube" : "spotify"}>
                {originApp == "spotify" ? "youtube" : "spotify"}
              </option>
            </select>
          </label>
        </div>

        <h2>Convert</h2>

        <form onSubmit={configurePlaylist} className="playlistForm">
          <input
            placeholder="Enter a playlist link..."
            onChange={(e) => setTitle(e.target.value)}
            className="playlistLinkInput"
          />
          <button type="submit" className="playlistLinkButton" ref={inputRef}>
            Next
          </button>
        </form>
        <div className="personal-playlists">
          <h2>Use your playlists instead</h2>

          <Authenticate
            setisLoading={setisLoading}
            inputRef={inputRef}
            seterror={seterror}
            error={error}
          />
        </div>
      </div>

      {configure && (
        <div className="configureWrapper">
          <Configure
            setisLoading={setisLoading}
            setconfigure={setconfigure}
            isLoading={isLoading}
            seterror={seterror}
            setsuccess={setsuccess}
          />
        </div>
      )}
    </div>
  );
};

export default Mainpage;
