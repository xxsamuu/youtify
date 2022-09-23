import React from "react";
import Playlist from "./Playlist";

const PlaylistWrapper = ({ playlistData, inputRef }) => {
  return (
    <div>
      {playlistData.map((item) => (
        <Playlist key={item.id} item={item} inputRef={inputRef} />
      ))}
    </div>
  );
};

export default PlaylistWrapper;
