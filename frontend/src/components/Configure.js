import React, { useState, useRef, useContext, useEffect } from "react";
import * as imageConversion from "image-conversion";
import { Context } from "../Context";

const Configure = ({
  setisLoading,
  setconfigure,
  isLoading,
  seterror,
  setsuccess,
}) => {
  const { originApp, playlistLink, setmessage } = useContext(Context);
  const [name, setname] = useState("");
  const [description, setdescription] = useState("");
  const [thumbnail, setthumbnail] = useState("");
  const imageRef = useRef();

  var intervalId;

  const createPlaylist = () => {
    console.log("createPlaylist fn");
    /*
    POST to API users customized data. In the backend, if those are blank, they will be set with their original values.
    getStatus() function calls API each one second to retrieve status of converting process.
    */
    intervalId = setInterval(() => {
      getStatus();
    }, 1000);
    console.log("playlist id: ", playlistLink);
    fetch("/api/main", {
      method: "POST",
      body: JSON.stringify({
        name,
        description,
        originApp,
        playlistLink: playlistLink,
        thumbnail,
      }),
      headers: {
        "Content-type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setsuccess("playlist created successfully");
        setisLoading(false);
        clearInterval(intervalId);
      })
      .catch((error) => {
        seterror("Error trying to reach the server. Try to refresh the page.");
        clearInterval(intervalId);
        setisLoading(false);
      });
    console.log(
      `posted data: ${name}, ${description}, ${originApp}, ${playlistLink}`
    );
  };

  async function getStatus() {
    fetch("/api/get-status")
      .then((res) => res.json())
      .then((data) => {
        setmessage(data.msg);
        seterror(data.error_data.error_msg);
        if (data.error_data.is_fatal === "True") {
          setconfigure(false);
        }
      })
      .catch((error) =>
        seterror(
          "error while trying to connect to the server. \nRefresh the page or try again."
        )
      );
  }

  const handlePlaylist = (e) => {
    /*
    check if input is blank, if not it calls function to create playlist.
    */
    e.preventDefault();
    setisLoading(true);
    if (e.target.value !== null) {
      console.log("here we are");
      createPlaylist();
      setconfigure(false);
    } else {
      alert("input cannot be blank.");
    }
    setname("");
    setdescription("");
  };

  const changeHandler = () => {
    /*
    Spotify needs the thumbnail to be in base64 jpeg format, and Youtube doesn't allow user-requested images
    as thumbnail. So, if image is not jpeg, use API to convert it to jpeg format.
    */
    const file = imageRef.current.files[0];

    const reader = new FileReader();
    const readerJPEG = new FileReader();

    reader.onload = (e) => {
      if (file.type === "image/jpeg") {
        setthumbnail(e.target.result);
      } else {
        imageConversion
          .dataURLtoFile(e.target.result, "image/jpeg")
          .then((data) => readerJPEG.readAsDataURL(data));
      }
    };
    reader.readAsDataURL(file);

    readerJPEG.onload = (e) => {
      setthumbnail(e.target.result);
    };
  };

  return (
    <div className="configure">
      <h1 className="heading">Configure your Playlist</h1>
      <div className="paramaters">
        <form onSubmit={(e) => handlePlaylist(e)}>
          <div className="title-div">
            <label>
              Name of the playlist:
              <input
                type="text"
                className="input"
                onChange={(e) => setname(e.target.value)}
                value={name}
              />
            </label>
          </div>
          <div className="description-div">
            <label>
              Description:
              <input
                type="text"
                className="input"
                onChange={(e) => setdescription(e.target.value)}
                value={description}
              />
            </label>
          </div>
          <div className="thumbnail-div" style={{ display: "flex" }}>
            <p>Thumbnail:</p>
            {/* that label will trigger event, even though input file is hidden
            and giving me possibility to style label.
            */}
            <label className="configureFormButton">
              Chose file
              <input
                type="file"
                className="inputFile"
                onChange={changeHandler}
                ref={imageRef}
                disabled={originApp === "spotify" ? true : false}
              />
            </label>
            <p className="thumbnail-warning">
              *Please note that a cover image can be added to a spotify playlist
              only.
            </p>
          </div>

          <button
            type="submit"
            className="convertPlaylist configureFormButton"
            disabled={isLoading}
          >
            Convert
          </button>
        </form>
      </div>
      <p className="p-warning">
        * note that if you leave inputs empty the values of the original
        playlist will be kept, and thumbnail would be the default one (spotify).
      </p>
    </div>
  );
};

export default Configure;
