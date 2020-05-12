import React from 'react';
import { Button, NavDropdown, Navbar, Nav } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faCaretDown, faEllipsisV } from '@fortawesome/free-solid-svg-icons'

import BrightnessSlider from './BrightnessSlider';
import TurnOffButton from './TurnOffButton';
import TurnOnButton from './TurnOnButton';


const Icon = (props) => {
    return (
        <p>
            Test
        </p>
    )
}


const Header = (props) => {
    let powerButton = props.currentlyOn
        ? <TurnOffButton turnOffVis={props.turnOffVis} />
        : <TurnOnButton turnOnVis={props.turnOnVis} />

    return (
        <Navbar bg="dark" variant="dark" expand="true">
            <NavDropdown id="collasible-nav-dropdown" title={<Button variant="dark"><FontAwesomeIcon icon={faBars} size='lg' /></Button>}>
                <NavDropdown.Item>Settings</NavDropdown.Item>
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