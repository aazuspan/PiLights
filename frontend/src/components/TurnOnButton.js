import React from 'react';
import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faPowerOff } from '@fortawesome/free-solid-svg-icons'


const TurnOnButton = (props) => {
    return (
        <Button className="secondary-button-outline" onClick={props.turnOn} title="Turn On" style={{ visibility: props.visibility }}>
            <FontAwesomeIcon icon={faPowerOff} />
        </Button>
    )
}

export default TurnOnButton;