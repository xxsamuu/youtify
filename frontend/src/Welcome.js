import React, { useEffect } from "react";
import { useNavigate } from "react-router";
import banner from "./images/banner.png";
const Welcome = ({ setisGreeted, isGreeted }) => {
  let navigate = useNavigate();
  useEffect(() => {
    if (JSON.parse(sessionStorage.getItem("isGreeted")) === true) {
      setisGreeted(true);
    }
  }, []);
  return (
    <div className="welcome-wrapper">
      <img src={banner} className="banner-img" />
      <div className="slogan-wrapper">
        <p>
          make your music <span>boundless.</span>
        </p>
      </div>
      <div className="button-wrapper">
        <button
          onClick={() => {
            setisGreeted(true);
            sessionStorage.setItem("isGreeted", true);
          }}
        >
          Get started
        </button>
      </div>
    </div>
  );
};

export default Welcome;
