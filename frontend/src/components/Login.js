import React, { useState, useEffect } from "react";
import { Redirect } from 'react-router-dom'
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";
import Alert from "react-bootstrap/Alert";
import "../stylesheets/Login.css";
import { useAppContext } from "../libs/contextLib";
import { useHistory, useLocation } from "react-router-dom";
import $ from 'jquery';

function Login () {

    const { userHasAuthenticated, setUser, user } = useAppContext();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    function validateForm() {
        return username.length > 0 && password.length > 0;
    }

    let history = useHistory();
    let location = useLocation();

    let { from } = location.state || { from: { pathname: null } };;


    useEffect(() => {}, [user]);


    function handleSubmit(event) {
        event.preventDefault();

        $.ajax({
          url: '/api/login',
          type: "POST",
          dataType: 'json',
          contentType: 'application/json',
          data: JSON.stringify({
            username: username,
            password: password
          }),
          xhrFields: {
            withCredentials: true
          },
          crossDomain: true,
          success: (result) => {
            userHasAuthenticated(true);
            setUser(result.user);
            return;
          },
          error: (error) => {
            var msg = 'Unable to login. Please try your request again.';
            if (error.responseJSON) {
                let reason;
                if (error.responseJSON.detailed_message) {
                    reason = error.responseJSON.detailed_message;
                } else {
                    reason = error.responseJSON.message;
                }
                msg += '\nReason: ' + reason
            }
            alert(msg)
            return;
          }
        })
    }


    return user ? (
        <Redirect to="/" />
    ) : (
        <>
        {from.pathname &&
            <Col sm={{ span: 12, offset: 4 }}>
              <Alert variant="danger" className="col-sm-4 center-block">
                You must log in to view the page at {from.pathname}
              </Alert>
            </Col>
        }
        <div className="AddForm">
          <Form onSubmit={handleSubmit}>
            <Form.Group size="lg" controlId="username">
              <Form.Label>Username</Form.Label>
              <Form.Control
                autoFocus
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </Form.Group>
            <Form.Group size="lg" controlId="password">
              <Form.Label>Password</Form.Label>
              <Form.Control
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </Form.Group>
            <Button block size="lg" type="submit" disabled={!validateForm()}>
              Login
            </Button>
          </Form>
        </div>
        </>
    );
}

export default Login;
