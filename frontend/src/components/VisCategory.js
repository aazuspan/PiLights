import React from 'react';


function VisCategory(props) {
    return (
        <button onClick={() => { props.filterVis(props.name) }} title={`Filter ${props.name}`} className="vis-box">
            <h5>{props.name}</h5>
        </button >
    )
}

export default VisCategory;