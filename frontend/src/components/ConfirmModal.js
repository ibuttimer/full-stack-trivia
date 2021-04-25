import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

function ConfirmModal(props) {
  return (
      <Modal show={props.isOpen} onHide={props.closeModal}>
        <Modal.Header closeButton>
          <Modal.Title>{props.title}</Modal.Title>
        </Modal.Header>
        <Modal.Body>{props.text}</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={props.closeModal}>
            {props.cancelText}
          </Button>
          <Button variant="primary" onClick={props.handleSubmit}>
            {props.confirmText}
          </Button>
        </Modal.Footer>
      </Modal>
  );
}

export default ConfirmModal;
