import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';

import TurnOffButton from './TurnOffButton';

const Header = (props) => {
    return (
        <Navbar bg="dark" variant="dark" expand="lg">
            <Navbar.Brand href="#home" className="mr-auto">Game Room Lights</Navbar.Brand>
            <Nav className="ml-auto">
                <TurnOffButton turnOffVis={props.turnOffVis} />
            </Nav>
        </Navbar>
    )
}

export default Header;