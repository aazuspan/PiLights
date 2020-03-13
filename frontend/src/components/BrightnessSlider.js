import axios from 'axios';
import React from 'react';



class BrightnessSlider extends React.Component {

    state = {
        brightness: '',
    }

    componentDidMount = () => {
        this.loadBrightnessFromMemory();
    }

    // Load the last saved brightness value from the backend permanent memory
    loadBrightnessFromMemory = () => {
        axios.get("http://127.0.0.1:5000", {
            params: {
                type: "loadMemory",
                attribute: 'brightness',
            }
        }).then((res) => {
            this.setState({
                brightness: res.data.brightness,
            });
        })
    }

    // Send the new brightness value to the backend to save in permanent memory
    saveBrightnessToMemory = () => {
        axios.get("http://127.0.0.1:5000", {
            params: {
                type: "saveMemory",
                attribute: 'brightness',
                value: this.state.brightness,
            }
        });
    }

    handleBrightnessChange = (event) => {
        this.setState({
            brightness: event.target.value
        }, this.saveBrightnessToMemory);
    }

    render() {
        return (
            <div className="brightness-slider">
                <label htmlFor="brightness" className="light">Brightness</label>
                <input type="range"
                    className="custom-range"
                    id="brightness"
                    min="10"
                    max="255"
                    step="5"
                    value={this.state.brightness}
                    onChange={this.handleBrightnessChange} />
            </div>
        )
    }
}

export default BrightnessSlider;