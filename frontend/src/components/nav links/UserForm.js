import React, { useContext, useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Card, Button, Form, Alert } from "react-bootstrap";
import auth from "../../firebase";
import { onAuthStateChanged } from "firebase/auth";
import { Context } from "../../Context";
const UserForm = ({
  clickHandler,
  action,
  seterror,
  error,
  setemail,
  setpassword,
  password,
  email,
}) => {
  let navigate = useNavigate();
  const [disabled, setdisabled] = useState(false);
  const { setisLoggedIn } = useContext(Context);
  useEffect(() => {
    seterror("");
  }, []);
  onAuthStateChanged(auth, (user) => {
    if (user) {
      console.log("logged in");
      setisLoggedIn(true);
      navigate("../", { replace: true });
    } else {
      console.log("logged out");
      setisLoggedIn(false);
    }
  });
  const checkPwd = (e) => {
    if (e.target.value !== password) {
      seterror("the two passwords don't match");
      setdisabled(true);
    } else {
      seterror("");
      setdisabled(false);
    }
  };
  const style = {
    height: error
      ? action === "login"
        ? "75%"
        : "90%"
      : action === "login"
      ? "70%"
      : "80%",
  };
  return (
    <div className="login-wrapper">
      <Card className="login-card" style={style}>
        <Card.Title className="title">
          {action === "login" ? "Login" : "Sign-up"}
        </Card.Title>
        <Card.Body>
          <Form
            onSubmit={(e) => {
              setdisabled(true);
              if (email === "" || password === "") {
                seterror("input must not be blank");
              }
              e.preventDefault();
              clickHandler();
            }}
          >
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address: </Form.Label>
              <Form.Control
                type="email"
                placeholder="Enter email"
                onChange={(e) => setemail(e.target.value)}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password: </Form.Label>
              <Form.Control
                type="password"
                placeholder="Password"
                onChange={(e) => setpassword(e.target.value)}
              />
            </Form.Group>
            {action == "signup" && (
              <Form.Group className="mb-3" controlId="formBasicPassword">
                <Form.Label>Confirm Password: </Form.Label>
                <Form.Control
                  type="password"
                  placeholder="Confirm Password"
                  onChange={(e) => checkPwd(e)}
                />
              </Form.Group>
            )}
            <p>
              {action === "login" ? "Don't" : "Already"} have an account?
              <Link
                to={action === "login" ? "/sign-up" : "/log-in"}
                className="link"
              >
                {action === "login" ? " Sign-in" : " Log-in"}
              </Link>
            </p>
            {error && <Alert variant="danger">{error}</Alert>}
            <Button type="submit" disabled={disabled}>
              Submit
            </Button>
          </Form>
        </Card.Body>
      </Card>
    </div>
  );
};

export default UserForm;
