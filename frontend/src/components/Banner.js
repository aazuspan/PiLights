import React from 'react';
import { Button } from 'react-bootstrap';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faStop } from '@fortawesome/free-solid-svg-icons'



function Banner(props) {
    let hiddenClass = props.currentVis ? "" : "banner-hidden"

    return (
        <div className={`banner ${hiddenClass}`}>
            <span className="contents">
                <span className="title">{props.currentVis ? props.currentVis.name : ""}</span>
                <span className="category" >{props.currentVis ? props.currentVis.category : ""}</span>
            </span>
            <span>
                <Button variant="warning" title="stop" className="float-right" onClick={props.stopVis}>
                    <FontAwesomeIcon icon={faStop} />
                </Button>
            </span>
        </div>
    )
}

export default Banner;