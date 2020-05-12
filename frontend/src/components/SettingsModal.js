import React from 'react';
import { Button, Modal } from 'react-bootstrap';

import BrightnessSlider from './BrightnessSlider';


const SettingsModal = (props) => {
    return (
        <Modal
            size="sm"
            aria-labelledby="contained-modal-title-vcenter"
            centered
            show={props.show}
            onHide={props.toggleSettings}
        >

            <Modal.Header closeButton>
                <Modal.Title id="contained-modal-title-vcenter">
                    Settings
                </Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <BrightnessSlider />
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.toggleSettings}>Close</Button>
                <Button variant="primary" onClick={props.toggleSettings}>Apply</Button>
            </Modal.Footer>
        </Modal>
    );
}


export default SettingsModal;