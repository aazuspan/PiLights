import React from 'react';
import axios from 'axios';

import Banner from './components/Banner';
import Header from './components/Header';
import SpinnerScreen from './components/SpinnerScreen';
import VisList from './components/VisList';

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
    this.showSpinner();

    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "startVis",
        visName: visName,
      }
    })
      .then((res) => {
        this.setState({
          currentVis: visName,
        });
        this.hideSpinner();
      })
  }

  turnOffVis = () => {
    this.showSpinner();

    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "stopVis",
      }
    })
      .then((res) => {
        this.setState({
          currentVis: null,
        });
        this.hideSpinner();
      })
  }

  hideSpinner = () => {
    this.setState({
      spinnerClass: 'display-none',
    })
  }

  showSpinner = () => {
    this.setState({
      spinnerClass: null,
    })
  }

  // Turns on the last played visualization
  turnOnVis = () => {
    // TODO: Set last played vis in local memory and load it
    this.startVis('Rain');
  }

  render() {
    let bannerContent = this.state.currentVis
      ? `Playing: ${this.state.currentVis} `
      : null

    let banner = this.state.currentVis
      ? <Banner content={bannerContent} />
      : null

    return (
      <>
        <SpinnerScreen spinnerClass={this.state.spinnerClass} />
        <Header turnOffVis={this.turnOffVis} turnOnVis={this.turnOnVis} currentlyOn={this.state.currentVis !== null} />
        {banner}
        <VisList list={this.state.list} startVis={this.startVis} />
      </>
    );
  }
}

export default App;
