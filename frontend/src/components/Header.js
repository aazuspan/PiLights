import React from 'react';
import { Button, NavDropdown, Navbar, Nav } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars } from '@fortawesome/free-solid-svg-icons'

import TurnOffButton from './TurnOffButton';
import TurnOnButton from './TurnOnButton';


const Header = (props) => {
    let powerButton = null;

    try {
        powerButton = props.currentlyOn
            ? <TurnOffButton turnOffVis={props.turnOff} visibility={props.switchedWemo.mac ? "visible" : "hidden"} />
            : <TurnOnButton turnOn={props.turnOn} visibility={props.switchedWemo.mac ? "visible" : "hidden"} />
    }
    catch (e) {
    }

    return (
        <Navbar fixed="top" bg="dark" variant="dark">
            <NavDropdown id="collasible-nav-dropdown" title={<Button variant="dark"><FontAwesomeIcon icon={faBars} size='lg' title="Options" /></Button>}>
                <NavDropdown.Item onClick={props.toggleSettings}>Settings</NavDropdown.Item>
                <NavDropdown.Item onClick={props.toggleWemo}>WEMO™ Control</NavDropdown.Item>
            </NavDropdown>

            <Navbar.Brand href="#home">
                Game Room
            </Navbar.Brand>
            <Nav className="ml-auto">
                {powerButton}
            </Nav>

        </Navbar >
    )
}

export default Header;