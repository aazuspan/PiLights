import React from 'react';


class BrightnessSlider extends React.Component {
    state = {
        brightness: 10,
    }

    //TODO: Load brightness from settings

    handleBrightnessChange = (event) => {
        this.setState({
            brightness: event.target.value
        })
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