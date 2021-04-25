import React, { useEffect } from "react";
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Jumbotron from 'react-bootstrap/Jumbotron'

import { useAppContext } from "../libs/contextLib";
import '../stylesheets/Home.css';

function Home() {

    const { isAuthenticated, user } = useAppContext();

    function userStats() {
        var percent = 0;
        if (user.num_questions > 0) {
            percent = Math.round(user.num_correct * 100 / user.num_questions)
        }
        return percent + '%';
    }

    useEffect(() => {}, [user, isAuthenticated]);

    function renderWelcome() {
      return (
        <Container>
          <Row>
            <Col md={{ span: 8, offset: 2 }}>
                <Jumbotron className="jumbo">
                    <h3>Hi {user.username}</h3>
                    <h5>Your current stats are:</h5>
                    <p>
                        {user.num_correct} questions out of {user.num_questions} answered correctly, i.e. {userStats()}
                    </p>
                </Jumbotron>
            </Col>
          </Row>
        </Container>
      )
    }

    function renderLogin() {
      return (
        <Container>
          <Row>
            <Col>
                <Jumbotron>
                    <h3>Please login to proceed.</h3>
                </Jumbotron>
            </Col>
          </Row>
        </Container>
      )
    }


    return user ? renderWelcome() : renderLogin();
}

export default Home;
