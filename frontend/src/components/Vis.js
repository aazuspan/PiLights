import React from 'react';
import { Button } from 'react-bootstrap';

function Vis(props) {
    return (
        <Button variant="info" onClick={() => { props.startVis(props.name) }} title={`Activate ${props.name}`} className="vis-box">
            <h5>{props.name}</h5>
            <hr />
            <p>{props.description}</p>
        </Button>
    )
}

export default Vis;