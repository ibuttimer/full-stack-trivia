import React, { useEffect } from "react";

import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Nav from 'react-bootstrap/Nav'
import Navbar from 'react-bootstrap/Navbar';
import Badge from 'react-bootstrap/Badge'
import { LinkContainer } from 'react-router-bootstrap'
import { useAppContext } from "../libs/contextLib";

import { useHistory } from "react-router-dom";

import '../stylesheets/Header.css';

function Header () {

    const history = useHistory();

    const { isAuthenticated, userHasAuthenticated, user, setUser } = useAppContext();

    useEffect(() => {
        document.title = 'Udacitrivia';
    });

    function handleLogout() {
        userHasAuthenticated(false);
        setUser(null);

        history.push("/login");
    }

    function userStats() {
        var percent = 0;
        if (user.num_questions > 0) {
            percent = Math.round(user.num_correct * 100 / user.num_questions)
        }
        return percent + '%';
    }

    return (
        <Container>
          <Row>
            <Col>
          <Navbar collapseOnSelect bg="primary" variant="dark" expand="md" className="mb-3">
            <LinkContainer to="/">
              <Navbar.Brand className="font-weight-bold text-muted">
                Udacitrivia
              </Navbar.Brand>
            </LinkContainer>
            <Navbar.Toggle />
            <Navbar.Collapse className="justify-content-center">
              <Nav activeKey={window.location.pathname}>
                {isAuthenticated ? (
                  <>
                    <LinkContainer to="/list">
                      <Nav.Link>List</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="/add">
                      <Nav.Link>Add</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="/play">
                      <Nav.Link>Play</Nav.Link>
                    </LinkContainer>
                    <Nav.Link onClick={handleLogout}>
                        Logout
                    </Nav.Link>
                  </>
                ) : (
                  <>
                    <LinkContainer to="/login">
                      <Nav.Link>Login</Nav.Link>
                    </LinkContainer>
                  </>
                )}
              </Nav>
              { user &&
                  <Navbar.Text className="ml-auto">
                      {user.username}&nbsp;
                      <Badge variant="light">{user.num_correct+"/"+ user.num_questions}</Badge><Badge variant="success">{userStats()}</Badge>
                  </Navbar.Text>
              }
            </Navbar.Collapse>
          </Navbar>
            </Col>
          </Row>
        </Container>
    );
}

export default Header;
