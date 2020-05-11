import React from 'react';
import { Form } from 'react-bootstrap';


// A switch control for a single Wemo
const WemoControl = (props) => {
    return (
        <>
            <Form.Switch
                type="switch"
                id={props.label}
                label={props.label}
                onChange={(event) => { console.log(event) }}
            />
            <br />
        </>
    )
}

export default WemoControl;