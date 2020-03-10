import React from 'react';
import axios from 'axios';

import TurnOffButton from './components/TurnOffButton';
import VisList from './components/VisList';

class App extends React.Component {

  state = {
    list: [],
    currentVis: 'Off',
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
      .then((res) => {
        this.setState({
          currentVis: visName,
        })
      })
  }

  turnOffVis = () => {
    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "stopVis",
      }
    })
      .then((res) => {
        this.setState({
          currentVis: 'Off',
        })
      })
  }

  render() {
    return (
      <>
        <h3>Currently playing: {this.state.currentVis}</h3>
        <TurnOffButton turnOffVis={this.turnOffVis} />
        <VisList list={this.state.list} startVis={this.startVis} />
      </>
    );
  }
}

export default App;
