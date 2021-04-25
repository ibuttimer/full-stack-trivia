import React, { Component } from 'react'
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

class Search extends Component {
    state = {
        query: '',
    }

    getInfo = (event) => {
        event.preventDefault();
        this.props.submitSearch(this.state.query)
        this.searchForm.reset();
    }

    handleInputChange = () => {
        this.setState({
            query: this.search.value
        })
    }

    validateForm = () => {
        return this.state.query.length > 0;
    }

    render() {
        return (
            <Form onSubmit={this.getInfo} ref={input => this.searchForm = input}>
                <Form.Group size="sm" controlId="search">
                    <Form.Control
                        type="text"
                        ref={input => this.search = input}
                        onChange={this.handleInputChange}
                    />
                </Form.Group>
                <Button block size="sm" type="submit" disabled={!this.validateForm()}>
                    Submit
                </Button>
            </Form>
        )
    }
}

export default Search
