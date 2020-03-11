import React from 'react';

import Vis from './Vis';
import VisCategory from './VisCategory'

class VisList extends React.Component {

    render() {
        this.visualizations = this.props.visList.map((vis) =>
            <li key={this.props.visList.indexOf(vis)}>
                <Vis
                    name={vis.name}
                    description={vis.description}
                    startVis={this.props.startVis}>
                </Vis>
            </li>
        )

        this.categories = this.props.categoryList.map((vis) =>
            <li key={this.props.categoryList.indexOf(vis)}>
                <VisCategory
                    name={vis.name}
                    filterVis={this.props.filterVis}>
                </VisCategory>
            </li>
        )

        // If a category is selected, show visualizations, otherwise show categories
        this.display = this.props.filter
            ? this.visualizations
            : this.categories

        return (
            <ul className="vis-list">
                {this.display}
            </ul>
        )
    }
}

export default VisList;