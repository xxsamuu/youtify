import { createUserWithEmailAndPassword } from "firebase/auth";
import React, { useState } from "react";
import auth from "../../firebase";
import UserForm from "./UserForm";
import { useNavigate } from "react-router-dom";
const Signup = ({ setisLoggedIn, setsuccess }) => {
  let navigate = useNavigate();
  const [error, seterror] = useState();
  const [email, setemail] = useState();
  const [password, setpassword] = useState();
  const signupHandler = () => {
    createUserWithEmailAndPassword(auth, email, password)
      .then((user) => setsuccess("user successfully created! "))
      .catch((error) => console.log(error.message) || seterror(error.message));
  };
  return (
    <>
      <UserForm
        clickHandler={signupHandler}
        action={"signup"}
        error={error}
        seterror={seterror}
        setemail={setemail}
        setpassword={setpassword}
        password={password}
        email={email}
        setisLoggedIn={setisLoggedIn}
      />
    </>
  );
};

export default Signup;
