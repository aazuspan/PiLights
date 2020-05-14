import React from 'react';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPowerOff } from '@fortawesome/free-solid-svg-icons'


const TurnOffButton = (props) => {
    return (
        <Button variant="danger" onClick={props.turnOffVis} title="Turn Off" style={{ visibility: props.visibility }}>
            <FontAwesomeIcon icon={faPowerOff} />
        </Button>
    )
}

export default TurnOffButton;