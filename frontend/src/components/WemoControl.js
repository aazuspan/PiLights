import React from 'react';
import { Form } from 'react-bootstrap';


// A switch control for a single Wemo
const WemoControl = (props) => {
    return (
        <Form.Switch
            type="switch"
            id={props.label}
            label={props.label}
            checked={props.checked}
            onChange={(event) => {
                props.setWemo(+ event.target.checked, props.mac);
            }}
        />
    )
}

export default WemoControl;