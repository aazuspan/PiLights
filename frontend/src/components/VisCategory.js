import React from 'react';
import { Button } from 'react-bootstrap';

function VisCategory(props) {
    return (
        <Button variant="info" onClick={() => { props.filterVis(props.name) }} title={`Filter ${props.name}`} className="vis-box">
            <h5>{props.name}</h5>
        </Button >
    )
}

export default VisCategory;