import React, { useContext, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import auth from "../firebase";
import { Context } from "../Context";
import logo from "../images/logo.svg";

const Nav = ({ opacity }) => {
  const { isLoggedIn, setisLoggedIn } = useContext(Context);
  let navigate = useNavigate();
  useEffect(() => {
    if (JSON.parse(sessionStorage.getItem("spotifyData")) === null) {
      navigate("../welcome", { replace: true });
    }
  }, []);

  return (
    <div className="nav-wrapper" style={opacity}>
      <Link to="/" className="link logo-link">
        <div className="logo-div">
          <img src={logo} />
          <h1>Youtify</h1>
        </div>
      </Link>
      <nav className="nav-links">
        {JSON.parse(localStorage.getItem("user")) ? (
          <p
            onClick={() => {
              auth.signOut();
              localStorage.removeItem("user");
            }}
            className="logout-p"
          >
            Log-out
          </p>
        ) : (
          <Link to="/log-in">Log-in</Link>
        )}
        <Link to="/info">Info</Link>
      </nav>
    </div>
  );
};

export default Nav;
