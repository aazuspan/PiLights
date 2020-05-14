import React from 'react';


function Banner(props) {
    return (
        <div className="banner" style={{ display: props.currentVis ? "" : "none" }}>
            <div><b>{props.currentVis ? props.currentVis.name : ""}</b></div>
            <div><small>{props.currentVis ? props.currentVis.category : ""}</small></div>
        </div>
    )
}

export default Banner;