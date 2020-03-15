import axios from 'axios';
import React from 'react';

import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';

class BrightnessSlider extends React.Component {

    state = {
        currentBrightness: '',
        savedBrightness: '',
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
                currentBrightness: res.data.brightness,
                savedBrightness: res.data.brightness,
            });
        })
    }

    // TODO: Have this sets brightness of pixels
    // Send the new brightness value to the backend to save in permanent memory
    saveBrightnessToMemory = () => {
        axios.get("http://127.0.0.1:5000", {
            params: {
                type: "saveMemory",
                attribute: 'brightness',
                value: this.state.currentBrightness,
            }
        })
            .then(() => {
                this.setState({
                    savedBrightness: this.state.currentBrightness,
                })
            })
    }

    handleBrightnessChange = (event) => {
        this.setState({
            currentBrightness: event.target.value
        });
    }

    render() {
        let updateDisabled = this.state.currentBrightness === this.state.savedBrightness;

        return (
            <div className="brightness-slider">
                <hr />
                <label htmlFor="brightness" className="light">Brightness</label>
                <input type="range"
                    className="custom-range"
                    id="brightness"
                    min="10"
                    max="255"
                    step="5"
                    value={this.state.currentBrightness}
                    onChange={this.handleBrightnessChange}
                />

                <Button onClick={this.saveBrightnessToMemory} disabled={updateDisabled}>
                    Update
                </Button>
            </div >
        )
    }
}

export default BrightnessSlider;