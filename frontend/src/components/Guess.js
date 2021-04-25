import React, { Component } from 'react'
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Col from "react-bootstrap/Col";

class Guess extends Component {
    state = {
        guess: '',
    }

    getInfo = (event) => {
        event.preventDefault();
        this.props.submitGuess(this.state.guess)
        this.guessForm.reset();
    }

    handleInputChange = () => {
        this.setState({
            guess: this.guess.value
        })
    }

    validateForm = () => {
        return this.state.guess.length > 0;
    }

    render() {
        return (
            <Form onSubmit={this.getInfo} ref={input => this.guessForm = input}>
                <Form.Group size="sm" controlId="search">
                    <Form.Control
                        type="text"
                        ref={input => this.guess = input}
                        onChange={this.handleInputChange}
                    />
                </Form.Group>
                <Col sm={{ span: 10, offset: 5 }}>
                    <Button block size="sm" type="submit"  className="col-sm-2" disabled={!this.validateForm()}>
                        Submit Answer
                    </Button>
                </Col>
            </Form>
        )
    }
}

export default Guess
