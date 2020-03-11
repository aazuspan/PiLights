import React from 'react';
import axios from 'axios';

import Header from './components/Header';
import SpinnerScreen from './components/SpinnerScreen';
import VisList from './components/VisList';
import { Spinner } from 'react-bootstrap';

class App extends React.Component {

  state = {
    list: [],
    currentVis: null,
    spinnerClass: 'display-none',
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
    this.setState({
      spinnerClass: null,
    })

    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "stopVis",
      }
    })
      .then((res) => {
        this.setState({
          currentVis: null,
          spinnerClass: 'display-none',
        })
      })
  }

  // Turns on the last played visualization
  turnOnVis = () => {
    // TODO: Set last played vis in local memory and load it
    this.startVis('Rain');
  }

  render() {
    return (
      <>
        <SpinnerScreen spinnerClass={this.state.spinnerClass} />
        <Header turnOffVis={this.turnOffVis} turnOnVis={this.turnOnVis} currentlyOn={this.state.currentVis !== null} />
        <h3>Currently playing: {this.state.currentVis}</h3>
        <VisList list={this.state.list} startVis={this.startVis} />
      </>
    );
  }
}

export default App;
