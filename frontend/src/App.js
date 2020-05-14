import React from 'react';
import axios from 'axios';
import { Breadcrumb } from 'react-bootstrap';

import Banner from './components/Banner';
import Header from './components/Header';
import SpinnerScreen from './components/SpinnerScreen';
import VisList from './components/VisList';
import WemoModal from './components/WemoModal';
import SettingsModal from './components/SettingsModal';
import * as settings from './settings';


class App extends React.Component {
  state = {
    visList: [],
    categoryList: [],
    filter: '',
    currentVis: null,
    on: false,
    spinnerClass: 'display-none',
    showWemo: false,
    showSettings: false,
    switchedWemo: null,
    wemos: [],
    settings: [],
  }

  componentDidMount = () => {
    this.getCategories();
    this.getWemos();
    this.getSettings();
    this.getStatus();
  }

  getStatus = () => {
    axios.get(settings.SERVER_ADDR + 'get-status/')
      .then((res) => {
        this.setState({
          on: res.data.on,
          currentVis: res.data.current_vis,
          switchedWemo: res.data.switched_wemo,
        });
      })
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

  // Get a list of all settings and their parameters
  getSettings = () => {
    axios.get(settings.SERVER_ADDR + 'load-settings/')
      .then((res) => {
        this.setState({
          settings: res.data.settings,
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

  // Turn off visualizations
  stopVis = () => {
    this.showSpinner();

    axios.get(settings.SERVER_ADDR + "stop-vis/")
      .then(() => {
        this.setState({
          currentVis: null,
        });
        this.hideSpinner();
      })
  }

  // Pass all updated settings to the API to be saved into memory
  saveSettings = (updatedSettings) => {
    axios.get(settings.SERVER_ADDR + "save-settings/", {
      params: {
        settings: JSON.stringify(updatedSettings),
      }
    }).then(
      // A delay is required between writing to settings and reading from settings
      setTimeout(this.getStatus, 100)
    );
  }

  // Turns on the switched WEMO
  turnOn = () => {
    axios.get(settings.SERVER_ADDR + "turn-on/")
      .then(() => {
        this.getStatus();
      });
  }

  // Turns off the switched WEMO
  turnOff = () => {
    axios.get(settings.SERVER_ADDR + "turn-off/")
      .then(() => {
        this.getStatus();
      });
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

  // Get the list of wemo devices, including names and mac addressed, from the API
  getWemos = () => {
    axios.get(settings.SERVER_ADDR + "get-wemos/")
      .then((res) => {
        this.setState({
          wemos: res.data.wemos,
        });
      })
  }

  // Toggle the Wemo control modal
  toggleWemo = (event) => {
    // Update the states of all Wemos
    this.getWemos();

    this.setState({
      showWemo: !this.state.showWemo,
    })
  }

  // Toggle the Settings modal
  toggleSettings = (event) => {
    this.getSettings();

    this.setState({
      showSettings: !this.state.showSettings,
    })
  }

  // Tell the API to rescan for WEMO devices
  rescanWemos = () => {
    this.showSpinner();
    axios.get(settings.SERVER_ADDR + "rescan-wemos/")
      .then(() => {
        this.getWemos();
        this.getStatus();
        this.hideSpinner();
      });
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
      this.getStatus();
    });
  }

  render() {
    let banner = this.state.currentVis
      ? <Banner content={`Playing: ${this.state.currentVis} `} />
      : null

    return (
      <>
        <SpinnerScreen spinnerClass={this.state.spinnerClass} />

        <WemoModal
          show={this.state.showWemo}
          toggleWemo={this.toggleWemo}
          setWemo={this.setWemo}
          wemos={this.state.wemos}
          rescanWemos={this.rescanWemos}
        />

        <SettingsModal
          show={this.state.showSettings}
          toggleSettings={this.toggleSettings}
          settings={this.state.settings}
          getSettings={this.getSettings}
          wemos={this.state.wemos}
          switchedWemo={this.state.switchedWemo}
          saveSettings={this.saveSettings}
        />

        <Header
          turnOff={this.turnOff}
          turnOn={this.turnOn}
          toggleWemo={this.toggleWemo}
          toggleSettings={this.toggleSettings}
          currentlyOn={this.state.on}
          switchedWemo={this.state.switchedWemo}
        />

        <Breadcrumb>
          <Breadcrumb.Item onClick={this.clearFilter} active={this.state.filter === ''}>Categories</Breadcrumb.Item>
          <Breadcrumb.Item active>{this.state.filter}</Breadcrumb.Item>
        </Breadcrumb>

        {banner}

        <VisList
          visList={this.state.visList}
          categoryList={this.state.categoryList}
          filter={this.state.filter}
          startVis={this.startVis}
          filterVis={this.filterVis} />
      </>
    );
  }
}

export default App;
