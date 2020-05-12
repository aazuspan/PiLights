import React from 'react';
import axios from 'axios';
import { Button, Modal } from 'react-bootstrap';

import SettingSlider from './SettingSlider';
import * as settings from '../settings';


class SettingsModal extends React.Component {
    // Pass all updated settings to the API to be saved into memory
    applySettings = () => {
        axios.get(settings.SERVER_ADDR + "save-settings/", {
            params: {
                settings: JSON.stringify(this.settings),
            }
        })
    }

    componentDidMount = () => {
        // Store a temporary list of updated setting values
        this.settings = {};
    }

    // Update the value of a setting with a given label
    updateSetting = (label, value) => {
        this.settings[label] = value;
    }

    render = () => {
        this.settingsSliders = this.props.settings.map((setting) =>
            <SettingSlider
                key={this.props.settings.indexOf(setting)}
                label={setting.label}
                minValue={setting.min_value}
                maxValue={setting.max_value}
                incrementValue={setting.increment_value}
                currentValue={setting.current_value}
                updateSetting={this.updateSetting}
            />
        );

        return (
            <Modal
                size="sm"
                aria-labelledby="contained-modal-title-vcenter"
                centered
                show={this.props.show}
                onHide={this.props.toggleSettings}
            >

                <Modal.Header closeButton>
                    <Modal.Title id="contained-modal-title-vcenter">
                        Settings
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {this.settingsSliders}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={this.props.toggleSettings}>Close</Button>
                    <Button variant="primary" onClick={this.applySettings}>Apply</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}


export default SettingsModal;