import React, { useState, useEffect } from "react";
import { Routes, BrowserRouter as Router, Route } from "react-router-dom";

import Login from "./components/nav links/Login";
import Info from "./components/nav links/Info";
import Signup from "./components/nav links/Signup";
import Nav from "./components/Nav";
import "bootstrap/dist/css/bootstrap.min.css";

import "./App.css";
import Mainpage from "./components/Mainpage";
import IsLoading from "./components/Redirect/IsLoading";
import { ContextProvider } from "./Context";
import Welcome from "./Welcome";
import Callback from "./components/Callback";

function App() {
  const [isLoading, setisLoading] = useState();
  const [error, seterror] = useState();
  const [success, setsuccess] = useState();

  useEffect(() => {
    if (isLoading == false) {
      setTimeout(() => {
        seterror("");
        setsuccess("");
      }, 2000);
    }
  }, [isLoading]);

  return (
    <>
      <ContextProvider>
        <Router>
          <Nav />
          <div className="not-navs">
            <Routes>
              <Route path="/welcome" element={<Welcome />} />
              <Route
                path="/"
                element={
                  <IsLoading
                    isLoading={isLoading}
                    Page={
                      <Mainpage
                        setisLoading={setisLoading}
                        isLoading={isLoading}
                        error={error}
                        seterror={seterror}
                        setsuccess={setsuccess}
                        success={setsuccess}
                      />
                    }
                  />
                }
              />

              <Route path="/log-in" element={<Login />} />
              <Route path="/sign-up" element={<Signup />} />
              <Route path="/info" element={<Info />} />
              <Route path="/callback" element={<Callback />} />
            </Routes>
          </div>
        </Router>
        {error && (
          <div className="error-wrapper msg-wrapper">
            <p className="error msg">{error}</p>
          </div>
        )}
        {success && (
          <div className="success-wrapper msg-wrapper">
            <p className="success msg">{success}</p>
          </div>
        )}
      </ContextProvider>
    </>
  );
}

export default App;
