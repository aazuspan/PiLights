import React from 'react';

function Banner(props) {
    return (
        <div className="banner">
            {props.content}
        </div>
    )
}

export default Banner;