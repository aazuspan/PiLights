import React from 'react';
import axios from 'axios';

import TurnOffButton from './components/TurnOffButton';
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

  turnOffVis = () => {
    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "stopVis",
      }
    })
  }

  render() {
    return (
      <>
        <TurnOffButton turnOffVis={this.turnOffVis} />
        <VisList list={this.state.list} startVis={this.startVis} />
      </>
    );
  }
}

export default App;
