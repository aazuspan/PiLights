import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

import BrightnessSlider from './BrightnessSlider';
import TurnOffButton from './TurnOffButton';
import TurnOnButton from './TurnOnButton';

const Header = (props) => {
    return (
        <Navbar bg="dark" variant="dark" expand="lg">
            <Nav className="mr-auto">
                <TurnOnButton turnOnVis={props.turnOnVis} />
            </Nav>
            <Navbar.Brand href="#home" className="mx-auto">Game Room Lights</Navbar.Brand>
            <Nav className="ml-auto">
                <TurnOffButton turnOffVis={props.turnOffVis} />
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