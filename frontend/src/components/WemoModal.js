import React from 'react';
import { Button, Modal } from 'react-bootstrap';
import WemoControl from './WemoControl';


const WemoModal = (props) => {
    let wemos = props.wemos.map((wemo) =>
        <WemoControl key={props.wemos.indexOf(wemo)} label={wemo.name} checked={wemo.state} setWemo={props.setWemo} mac={wemo.mac} />
    )

    if (!wemos) {
        wemos = <p>No WEMO™ devices were found.</p>
    }

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
                {wemos}
            </Modal.Body>
            <Modal.Footer>
                <Button onClick={props.toggleWemo}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}


export default WemoModal;