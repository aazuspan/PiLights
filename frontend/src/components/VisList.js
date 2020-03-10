import React from 'react';

import Vis from './Vis';

class VisList extends React.Component {

    render() {
        this.visualizations = this.props.list.map((vis) =>
            <Vis
                key={this.props.list.indexOf(vis)}
                name={vis.name}
                description={vis.description}
                startVis={this.props.startVis}>
            </Vis>)

        return (
            <>
                {this.visualizations}
            </>
        )
    }
}

export default VisList;