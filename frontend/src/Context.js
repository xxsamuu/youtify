import React, { createContext, useEffect, useState } from "react";

const Context = createContext(
  {},
  () => "",
  () => {}
);

const ContextProvider = (props) => {
  const [title, setTitle] = useState();
  const [isLoggedIn, setisLoggedIn] = useState(false);
  const [message, setmessage] = useState("Loading...");
  //to check wheter we're converting form spotify to youtube or the other way around.
  const [originApp, setOriginApp] = useState("spotify");
  //if user doesnt click on playlist and instead submit a form, the default value would be the link submitted. Otherwise, it's the link of playlist clicked.
  const [playlistLink, setplaylistLink] = useState(title);
  const [playlistImage, setplaylistImage] = useState();
  //to check if link passed in input is from clicking on a playlist or passing a link of its own.
  const [isFromPlaylist, setisFromPlaylist] = useState(false);
  const states = {
    title,
    setTitle,
    isLoggedIn,
    setisLoggedIn,
    originApp,
    setOriginApp,
    playlistLink,
    setplaylistLink,
    playlistImage,
    setplaylistImage,
    message,
    setmessage,
    isFromPlaylist,
    setisFromPlaylist,
  };
  return <Context.Provider value={states}>{props.children}</Context.Provider>;
};

export { ContextProvider, Context };
