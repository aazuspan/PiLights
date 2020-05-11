import React from 'react';
import { Button, Modal } from 'react-bootstrap';
import WemoControl from './WemoControl';


const WemoModal = (props) => {
    return (
        <Modal
            size="sm"
            aria-labelledby="contained-modal-title-vcenter"
            centered
            show={props.show}
            onHide={props.toggleWemo}
        >

            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    WEMO™ Control
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <WemoControl label="Ceiling Lights" checked={true} />
                <WemoControl label="Bar Lights" checked={false} />
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.toggleWemo}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}


export default WemoModal;