import React from 'react';
import { Button, Form, Modal } from 'react-bootstrap';

import SettingSlider from './SettingSlider';


class SettingsModal extends React.Component {
    componentDidMount = () => {
        // Store a temporary list of updated setting values
        this.settings = {};
    }

    componentDidUpdate = () => {
        this.settingsSliders = this.props.settings.map((setting) =>
            setting.type === "slider" ?
                <SettingSlider
                    key={this.props.settings.indexOf(setting)}
                    label={setting.label}
                    minValue={setting.min_value}
                    maxValue={setting.max_value}
                    incrementValue={setting.increment_value}
                    currentValue={setting.current_value}
                    updateSetting={this.updateSetting}
                />
                :
                null
        );

        this.wemoOptions = this.props.wemos.map((wemo) =>
            <option
                key={this.props.wemos.indexOf(wemo)}
                mac={wemo.mac}>
                {wemo.name}
            </option>
        );
    }

    // Update the value of a setting with a given label
    updateSetting = (label, value) => {
        this.settings[label] = value;
    }

    // Handle changes to the switched WEMO select form
    handleSelectChange = (event) => {
        let option = event.target.childNodes[event.target.selectedIndex];
        let currentValue = { mac: option.getAttribute('mac'), label: option.value };
        this.updateSetting('switch_wemo', currentValue);
    }

    render = () => {
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
                    <Form.Group controlId="powerWemo" title='Select a WEMO for automatic power control.'>
                        <Form.Label>Switched WEMO™</Form.Label>
                        <Form.Control as="select" onChange={this.handleSelectChange} defaultValue={this.props.switchedWemo ? this.props.switchedWemo.label : "None"}>
                            <option>None</option>
                            {this.wemoOptions}
                        </Form.Control>
                    </Form.Group>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={this.props.toggleSettings}>Close</Button>
                    <Button variant="primary" onClick={() => { this.props.saveSettings(this.settings) }}>Apply</Button>
                </Modal.Footer>
            </Modal>
        );
    }
}


export default SettingsModal;