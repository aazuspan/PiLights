import React from 'react';
import { Button, Modal } from 'react-bootstrap';
import WemoControl from './WemoControl';


const WemoModal = (props) => {
    return (
        <Modal
            {...props}
            size="lg"
            aria-labelledby="contained-modal-title-vcenter"
            centered
        >
            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Wemo Control
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <WemoControl label="Ceiling Lights" />
                <WemoControl label="Bar Lights" />
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.onHide}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}


export default WemoModal;