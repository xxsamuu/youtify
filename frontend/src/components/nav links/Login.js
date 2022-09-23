import { signInWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import auth from "../../firebase";
import UserForm from "./UserForm";
import { useNavigate } from "react-router";

const Login = ({ isLoggedIn, setisLoggedIn, setsuccess }) => {
  let navigate = useNavigate();

  const [error, seterror] = useState();
  const [email, setemail] = useState();
  const [password, setpassword] = useState();

  const loginHandler = () => {
    signInWithEmailAndPassword(auth, email, password)
      .then((user) => {
        console.log(user.user);
        localStorage.setItem("user", JSON.stringify(user.user));
        setsuccess("user successfully logged in! ");
      })
      .catch((error) => {
        console.log(error.message);
        seterror(error.message);
      });
    console.log(isLoggedIn);
  };
  return (
    <>
      <UserForm
        clickHandler={loginHandler}
        action="login"
        error={error}
        seterror={seterror}
        isLoggedIn={isLoggedIn}
        setemail={setemail}
        setpassword={setpassword}
        password={password}
        email={email}
        setisLoggedIn={setisLoggedIn}
      />
    </>
  );
};

export default Login;
