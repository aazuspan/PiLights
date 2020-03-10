import React from 'react';


function Vis(props) {
    return (
        <button onClick={() => { props.startVis(props.name) }}>
            <h3>{props.name}</h3>
            <hr />
            <p>{props.description}</p>
        </button>
    )
}

export default Vis;