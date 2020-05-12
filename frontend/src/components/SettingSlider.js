import React from 'react';


class SettingSlider extends React.Component {
    state = {
        currentValue: this.props.currentValue,
    }

    handleChange = (event) => {
        this.setState({
            currentValue: event.target.value
        });
        this.props.updateSetting(this.props.label, event.target.value);
    }

    render() {
        return (
            <div className="settings-slider">
                <label htmlFor={this.props.label}>{this.props.label}</label>
                <input type="range"
                    className="custom-range"
                    id={this.props.label}
                    min={this.props.minValue}
                    max={this.props.maxValue}
                    step={this.props.incrementValue}
                    value={this.state.currentValue}
                    onChange={this.handleChange}
                />
            </div >
        )
    }
}

export default SettingSlider;