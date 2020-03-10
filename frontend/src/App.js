import React from 'react';
import axios from 'axios';

import VisList from './components/VisList';

class App extends React.Component {

  state = {
    list: [],
  }

  componentDidMount = () => {
    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "getList",
      }
    }).then((res) => {
      this.setState({
        list: res.data.list,
      });
    })
  }

  startVis = (visName) => {
    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "startVis",
        visName: visName,
      }
    })
  }

  render() {
    return (
      <VisList list={this.state.list} startVis={this.startVis} />
    );
  }
}

export default App;
