import React from 'react';
import axios from 'axios';
import Breadcrumb from 'react-bootstrap/Breadcrumb';

import Banner from './components/Banner';
import Header from './components/Header';
import SpinnerScreen from './components/SpinnerScreen';
import VisList from './components/VisList';

class App extends React.Component {

  state = {
    visList: [],
    categoryList: [],
    filter: '',
    currentVis: null,
    spinnerClass: 'display-none',
  }

  componentDidMount = () => {
    this.getLists()
  }

  // Get and set list of visualizations and categories
  getLists = (filterCategory = '') => {
    axios.get("http://127.0.0.1:5000", {
      params: {
        type: "getList",
        filter: filterCategory,
      }
    }).then((res) => {
      this.setState({
        filter: filterCategory,
        visList: res.data.vis_list,
        categoryList: res.data.category_list,
      });
    })
  }

  // Start rendering a specific visualization
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

  // Turn off all visualizations
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

  // Add a category filter to visualizations
  filterVis = (categoryName) => {
    this.getLists(categoryName);
  }

  // Clear the category filter
  clearFilter = () => {
    this.setState({
      filter: '',
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
        <SpinnerScreen spinnerClass={this.state.spinnerClass} />
        <Header turnOffVis={this.turnOffVis} turnOnVis={this.turnOnVis} currentlyOn={this.state.currentVis !== null} />

        <Breadcrumb>
          <Breadcrumb.Item onClick={this.clearFilter}>Categories</Breadcrumb.Item>
          {breadcrumbCategory}
        </Breadcrumb>

        {banner}
        <VisList visList={this.state.visList} categoryList={this.state.categoryList} startVis={this.startVis} filter={this.state.filter} filterVis={this.filterVis} />
      </>
    );
  }
}

export default App;
