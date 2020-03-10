import React from 'react';

import Vis from './Vis';

class VisList extends React.Component {

    render() {
        this.visualizations = this.props.list.map((vis) =>
            <li key={this.props.list.indexOf(vis)}>
                <Vis
                    name={vis.name}
                    description={vis.description}
                    startVis={this.props.startVis}>
                </Vis>
            </li>
        )

        return (
            <ul>
                {this.visualizations}
            </ul>
        )
    }
}

export default VisList;