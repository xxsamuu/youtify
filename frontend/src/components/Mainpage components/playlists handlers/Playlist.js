import React, { useContext, useState } from "react";
import { Context } from "../../../Context";
const Playlist = ({ item, inputRef }) => {
  const [image, setimage] = useState(item.image[0].url);
  const {
    setTitle,
    title,
    originApp,
    setplaylistLink,
    setplaylistImage,
    setisFromPlaylist,
  } = useContext(Context);

  const clickHandler = () => {
    console.log("click handler called");
    setisFromPlaylist(true);
    setTitle(item.playlist_url);
    inputRef.current.click();
    console.log(title);

    if (originApp == "spotify") {
      setplaylistLink(item.playlist_url);
      setplaylistImage(image);
    } else {
      setplaylistLink(item.id);
      setplaylistImage(item.image);
    }
  };
  return (
    <div className="playlist-item" onClick={clickHandler}>
      {
        <div className="playlist">
          <img
            src={originApp === "spotify" ? image : item.image}
            alt="playlist image"
          />
          <p>{item.playlist_name}</p>
        </div>
      }
    </div>
  );
};

export default Playlist;
