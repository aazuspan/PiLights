import React from 'react';
import { Spinner } from 'react-bootstrap';


function SpinnerScreen(props) {
    return (
        <div className="spinner-screen" style={{ visibility: props.show ? "visible" : "hidden" }}>
            <Spinner animation="border" role="status">
                <span className="sr-only">Loading...</span>
            </Spinner>
        </div>
    )
}

export default SpinnerScreen;