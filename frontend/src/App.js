import React from 'react';
import axios from 'axios';
import { Breadcrumb } from 'react-bootstrap';

import Banner from './components/Banner';
import Header from './components/Header';
import SpinnerScreen from './components/SpinnerScreen';
import VisList from './components/VisList';
import WemoModal from './components/WemoModal';
import * as settings from './settings';


class App extends React.Component {

  state = {
    visList: [],
    categoryList: [],
    filter: '',
    currentVis: null,
    spinnerClass: 'display-none',
    showWemo: false,
    wemos: [],
  }

  componentDidMount = () => {
    this.getCategories();
    this.getWemos();
  }

  // Get and set list of categories and current visualization playing
  getCategories = () => {
    axios.get(settings.SERVER_ADDR)
      .then((res) => {
        this.setState({
          categoryList: res.data.category_list,
          currentVis: res.data.current_vis,
        });
      })
  }

  getWemos = () => {
    axios.get(settings.SERVER_ADDR + 'get-wemos/')
      .then((res) => {
        this.setState({
          wemos: res.data.wemos,
        });
      })
  }

  // Start rendering a specific visualization
  startVis = (visName) => {
    this.showSpinner();

    axios.get(settings.SERVER_ADDR + "start-vis/", {
      params: {
        visName: visName,
      }
    })
      .then(() => {
        this.setState({
          currentVis: visName,
        });
        this.hideSpinner();
      })
  }

  // Turn off all visualizations
  turnOffVis = () => {
    this.showSpinner();

    axios.get(settings.SERVER_ADDR + "stop-vis/")
      .then(() => {
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
    axios.get(settings.SERVER_ADDR + "load-memory/", {
      params: {
        attribute: 'last_visualization',
      }
    }).then((res) => {
      this.startVis(res.data.value);
    })
  }

  // Add a category filter to visualizations
  filterVis = (categoryName) => {
    axios.get(settings.SERVER_ADDR + "filter/", {
      params: {
        category: categoryName,
      }
    }).then((res) => {
      this.setState({
        filter: categoryName,
        visList: res.data.vis_list,
      });
    })
  }

  // Clear the category filter
  clearFilter = () => {
    this.setState({
      filter: '',
    });
  }

  // Toggle the Wemo control modal
  toggleWemo = (event) => {
    // Update the states of all Wemos
    this.getWemos();

    this.setState({
      showWemo: !this.state.showWemo,
    })
  }

  // Set the power state of a Wemo device based on its MAC address
  setWemo = (newState, mac) => {
    axios.get(settings.SERVER_ADDR + "set-wemo/", {
      params: {
        state: newState,
        mac: mac,
      }
    }).then(() => {
      this.getWemos();
    });
  }

  render() {
    let bannerContent = this.state.currentVis
      ? `Playing: ${this.state.currentVis} `
      : null

    let banner = this.state.currentVis
      ? <Banner content={bannerContent} />
      : null

    let breadcrumbCategory = this.state.filter
      ? <Breadcrumb.Item active>{this.state.filter}</Breadcrumb.Item>
      : null

    return (
      <>
        <WemoModal
          show={this.state.showWemo}
          toggleWemo={this.toggleWemo}
          setWemo={this.setWemo}
          wemos={this.state.wemos}
        />

        <SpinnerScreen spinnerClass={this.state.spinnerClass} />

        <Header
          turnOffVis={this.turnOffVis}
          turnOnVis={this.turnOnVis}
          toggleWemo={this.toggleWemo}
          currentlyOn={this.state.currentVis !== null}
        />

        <Breadcrumb>
          <Breadcrumb.Item onClick={this.clearFilter} active={this.state.filter === ''}>Categories</Breadcrumb.Item>
          {breadcrumbCategory}
        </Breadcrumb>

        {banner}
        <VisList
          visList={this.state.visList}
          categoryList={this.state.categoryList}
          startVis={this.startVis}
          filter={this.state.filter}
          filterVis={this.filterVis} />
      </>
    );
  }
}

export default App;
