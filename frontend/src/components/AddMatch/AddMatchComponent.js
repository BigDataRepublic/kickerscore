import React, { Component } from "react";
import { Input, Button, InputGroup } from "reactstrap";
import PropTypes from "prop-types";

const range = (start, end) =>
    Array.from(Array(end).keys()).map(val => val + start);

export default class AddMatchComponent extends Component {
    state = {
        matchJustAdded: false
    };

    addMatch = () =>
        this.props
            .onAddMatch(
                parseInt(this.bluePoints.value),
                parseInt(this.redPoints.value)
            )
            .then(() => this.setState({ matchJustAdded: true }));

    renderInputOption = val => <option key={val}>{val}</option>;

    renderButton = (onClick, text, disabled, color = "secondary") => (
        <Button
            color={color}
            style={{ width: "30%", borderRadius: 0 }}
            disabled={disabled}
            onClick={onClick}
        >
            {text}
        </Button>
    );

    renderReMatchButton = () => {
        const resetComponent = () => {
            this.setState({ matchJustAdded: false });
            this.bluePoints.value = "0";
            this.redPoints.value = "0";
        };
        return this.renderButton(
            resetComponent,
            "Add another",
            false,
            "success"
        );
    };

    renderAddMatchButton = () => {
        const buttonContent = this.props.addingMatch ? "..." : "Add match";
        return this.renderButton(
            this.addMatch,
            buttonContent,
            !this.props.canAddMatch
        );
    };

    render() {
        const { matchJustAdded } = this.state;
        return (
            <InputGroup
                className="mx-auto"
                style={{
                    maxWidth: "80%",
                    marginTop: "2em",
                    marginBottom: "2em"
                }}
            >
                <Input
                    type="select"
                    name="redPoints"
                    innerRef={input => (this.redPoints = input)}
                    placeholder="with a placeholder"
                    style={{ borderRadius: 0, WebkitAppearance: "none" }}
                >
                    {range(0, 16).map(this.renderInputOption)}
                </Input>
                {matchJustAdded
                    ? this.renderReMatchButton()
                    : this.renderAddMatchButton()}
                <Input
                    type="select"
                    name="bluePoints"
                    innerRef={input => (this.bluePoints = input)}
                    placeholder="with a placeholder"
                    style={{ borderRadius: 0, WebkitAppearance: "none" }}
                >
                    {range(0, 16).map(this.renderInputOption)}
                </Input>
            </InputGroup>
        );
    }
}

AddMatchComponent.propTypes = {
    onAddMatch: PropTypes.func.isRequired,
    canAddMatch: PropTypes.bool.isRequired,
    addingMatch: PropTypes.bool.isRequired
    // TODO: make it more like this instead of mixing many booleans
    // matchStatus: PropTypes.oneOf([null, "ADDING", "ADDED"])
};
