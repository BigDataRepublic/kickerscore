import React, { Component } from "react";
import { Input, Button, InputGroup } from "reactstrap";
import PropTypes from "prop-types";

const range = (start, end) =>
    Array.from(Array(end).keys()).map(val => val + start);

export default class AddMatchComponent extends Component {
    renderInputOption = val => <option key={val}>{val}</option>;

    render() {
        const { canAddMatch, onAddMatch, addingMatch } = this.props;
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
                >
                    {range(0, 16).map(this.renderInputOption)}
                </Input>
                <Button
                    style={{ width: "30%" }}
                    disabled={!canAddMatch}
                    onClick={() =>
                        onAddMatch(this.bluePoints.value, this.redPoints.value)
                    }
                >
                    Add match
                </Button>
                <Input
                    type="select"
                    name="bluePoints"
                    innerRef={input => (this.bluePoints = input)}
                    placeholder="with a placeholder"
                >
                    {range(0, 16).map(this.renderInputOption)}
                </Input>
            </InputGroup>
        );
    }
}

AddMatchComponent.propTypes = {
    onAddMatch: PropTypes.func,
    canAddMatch: PropTypes.bool,
    addingMatch: PropTypes.bool
};
