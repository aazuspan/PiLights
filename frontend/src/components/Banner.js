import React from 'react';

function Banner(props) {
    return (
        <div className="banner">
            {props.currentVis}
        </div>
    )
}

export default Banner;