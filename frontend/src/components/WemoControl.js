import React from 'react';
import { Form } from 'react-bootstrap';


// A switch control for a single Wemo
const WemoControl = (props) => {
    return (
        <Form.Switch
            type="switch"
            id={props.label}
            label={props.label}
            // checked={props.checked}
            onChange={(event) => { console.log('test') }}
        />
    )
}

export default WemoControl;