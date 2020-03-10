import React from 'react';


function Vis(props) {
    return (
        <button onClick={() => { props.startVis(props.name) }} title={`Activate ${props.name}`}>
            <h5>{props.name}</h5>
            <hr />
            <p>{props.description}</p>
        </button >
    )
}

export default Vis;