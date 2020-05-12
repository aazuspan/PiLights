import React from 'react';
import { Button, Modal } from 'react-bootstrap';

import SettingSlider from './SettingSlider';

const SettingsModal = (props) => {
    let settings = props.settings.map((setting) =>
        <SettingSlider
            key={props.settings.indexOf(setting)}
            label={setting.label}
            minValue={setting.min_value}
            maxValue={setting.max_value}
            incrementValue={setting.increment_value}
            currentValue={setting.current_value}
        />
    )

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
                {settings}
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={props.toggleSettings}>Close</Button>
                <Button variant="primary" onClick={props.toggleSettings}>Apply</Button>
            </Modal.Footer>
        </Modal>
    );
}


export default SettingsModal;