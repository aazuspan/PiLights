import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

import BrightnessSlider from './BrightnessSlider';
import TurnOffButton from './TurnOffButton';
import TurnOnButton from './TurnOnButton';

const Header = (props) => {
    let powerButton = props.currentlyOn ? <TurnOffButton turnOffVis={props.turnOffVis} /> : <TurnOnButton turnOnVis={props.turnOnVis} />

    return (
        <Navbar bg="dark" variant="dark" expand="lg">
            <Navbar.Brand href="#home" className="mx-auto">Game Room Lights</Navbar.Brand>
            <Nav className="ml-auto">
                {powerButton}
            </Nav>

            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mr-auto">
                    <BrightnessSlider />
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}

export default Header;