import axios from 'axios';
import React from 'react';

import Button from 'react-bootstrap/Button';
import * as settings from '../settings';

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
        axios.get(settings.SERVER_ADDR + "load-memory/", {
            params: {
                attribute: 'brightness',
            }
        }).then((res) => {
            this.setState({
                currentBrightness: res.data.value,
                savedBrightness: res.data.value,
            });
        })
    }

    // Send the new brightness value to the backend to save in permanent memory
    saveBrightnessToMemory = () => {
        axios.get(settings.SERVER_ADDR + "set-brightness/", {
            params: {
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
                <label htmlFor="brightness">Brightness</label>
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