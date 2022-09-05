import React from "react";
import { useNavigate } from "react-router";
import banner from "./images/banner.png";
const Welcome = () => {
  let navigate = useNavigate();
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
            navigate("../", { replace: true });
            JSON.stringify(sessionStorage.setItem("welcome", true));
          }}
        >
          Get started
        </button>
      </div>
    </div>
  );
};

export default Welcome;
