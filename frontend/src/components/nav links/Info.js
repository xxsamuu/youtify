import React from "react";

const Info = () => {
  return (
    <div>
      <div className="personal-information">
        <h2>Who am I?</h2>
        <p>
          I'm a 16 years old programmer (full stack developer) passionate about
          all of what concerns tech. Other than programming, i'm interested and
          learning about Cyber-security. I code in many languages, like
          Javascfript (react, more precisely), Python, PHP and by the time
          you're reading this, probably C++ too.
        </p>
      </div>
      <div className="project-information">
        <h2>About the project</h2>
        <p>
          This project works both on the frontend and the backend; The Frontend
          fully delegates all of the fetching and logic to the server-side,
          written in Python and communicating with the client-side via Python's
          microframework Flask. It also relies on Google's Firebase library for
          what concerns authentication, The Youtube Data API for all of the
          actions concerning Youtube, and the Python-friendly API Spotipy for
          actions regarding Spotify. For a full understanding on how this
          website works, you can see the source code in my Github Repo.
        </p>
      </div>
    </div>
  );
};

export default Info;
