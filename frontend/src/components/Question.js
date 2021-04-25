import React, { Component } from 'react';
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Accordion from "react-bootstrap/Accordion";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";
import { RiDeleteBinLine } from 'react-icons/ri';
import { GiThink } from 'react-icons/gi';
import AppIcon from './AppIcon';
import ConfirmModal from './ConfirmModal';

import '../stylesheets/Question.css';

class Question extends Component {

  constructor(){
    super();
    this.state = {
      modalShow : false
    }
  }

    openModal = () => this.setState({ modalShow: true });
    closeModal = () => this.setState({ modalShow: false });
    handleSubmit = (qid) => {
        this.setState({ modalShow: false });
        this.props.questionAction(qid, 'DELETE')
    }


  render() {
    const { qid, question, answer, category, difficulty } = this.props;
    return (
        <Accordion>
            <Card border="dark">
                <Card.Header>
                    <OverlayTrigger
                          key="top"
                          placement="top"
                          overlay={
                            <Tooltip id="tooltip-${qid}">
                              Click to reveal answer
                            </Tooltip>
                          }
                        >
                        <Accordion.Toggle as={Card.Header} eventKey="0">
                            {question}
                        </Accordion.Toggle>
                    </OverlayTrigger>
                </Card.Header>
                <Container className="tb-margin">
                    <Row>
                        <Col><AppIcon sel_icon={category} fontSize="1.5em"/> {category}</Col>
                        <Col><GiThink fontSize="1.5em"/> {difficulty}</Col>
                        <Col>
                            <Button variant="default" onClick={this.openModal}>
                                <RiDeleteBinLine fontSize="1.5em"/>
                            </Button>
                            { this.state.modalShow ?
                                <ConfirmModal
                                        isOpen={this.state.modalShow}
                                        closeModal={this.closeModal}
                                        handleSubmit={() => this.handleSubmit(qid)}
                                        title="Delete Confirmation"
                                        text="Are you sure you want to delete this question?"
                                        cancelText="Cancel"
                                        confirmText="Delete"
                                        />
                                      :
                                      null
                            }
                        </Col>
                    </Row>
                </Container>
                <Accordion.Collapse eventKey="0">
                    <Card.Body>{answer}</Card.Body>
                </Accordion.Collapse>
            </Card>
        </Accordion>
    );
  }
}

export default Question;
