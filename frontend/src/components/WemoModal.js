import React from 'react';
import { Button, Modal } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSyncAlt } from '@fortawesome/free-solid-svg-icons'

import WemoControl from './WemoControl';


const WemoModal = (props) => {
    let wemos = props.wemos.map((wemo) =>
        <WemoControl key={props.wemos.indexOf(wemo)} label={wemo.name} checked={wemo.state} setWemo={props.setWemo} mac={wemo.mac} />
    )

    if (wemos.length === 0) {
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
                <Button variant="secondary" className="mr-auto" onClick={props.rescanWemos}><FontAwesomeIcon icon={faSyncAlt} size='lg' title="Rescan" /></Button>
                <Button variant="secondary" onClick={props.toggleWemo}>Close</Button>
            </Modal.Footer>
        </Modal>
    );
}


export default WemoModal;
