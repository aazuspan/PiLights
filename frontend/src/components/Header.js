import React from 'react';
import { Button, Navbar, Nav } from 'react-bootstrap';

import BrightnessSlider from './BrightnessSlider';
import TurnOffButton from './TurnOffButton';
import TurnOnButton from './TurnOnButton';


const Header = (props) => {
    let powerButton = props.currentlyOn
        ? <TurnOffButton turnOffVis={props.turnOffVis} />
        : <TurnOnButton turnOnVis={props.turnOnVis} />

    return (
        <Navbar bg="dark" variant="dark" expand="true">
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Brand href="#home">
                Game Room
            </Navbar.Brand>
            <Nav className="ml-auto">
                {powerButton}
            </Nav>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav>
                    <BrightnessSlider />
                </Nav>
                <Nav>
                    <Button onClick={props.toggleWemo}>WEMO™ Control</Button>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    )
}

export default Header;