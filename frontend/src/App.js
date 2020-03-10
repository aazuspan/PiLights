import React from 'react';
import axios from 'axios';

import VisList from './components/VisList';

class App extends React.Component {

  state = {
    list: [],
  }

  componentDidMount = () => {
    axios.get("http://127.0.0.1:5000", {
      type: "get_list"
    }).then((res) => {
      this.setState({
        list: res.data.list,
      });
    })
  }

  startVis = (visName) => {
    // TODO: Make get request with this name to activate the render method for that vis
    console.log(visName);
  }

  render() {
    return (
      <VisList list={this.state.list} startVis={this.startVis} />
    );
  }
}

export default App;
