import React from 'react';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPowerOff } from '@fortawesome/free-solid-svg-icons'


const TurnOnButton = (props) => {
    return (
        <Button variant="success" onClick={props.turnOnVis} title="Turn On">
            <FontAwesomeIcon icon={faPowerOff} />
        </Button>
    )
}

export default TurnOnButton;