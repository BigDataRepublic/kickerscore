import React, { Component } from "react";
import { Input, Button, InputGroup } from "reactstrap";

const range = (start, end) =>
    Array.from(Array(end).keys()).map(val => val + start);

export default class AddMatchComponent extends Component {
    renderInputOption = val => <option key={val}>{val}</option>;

    render() {
        return (
            <InputGroup>
                <Input
                    type="select"
                    name="redPoints"
                    innerRef={input => (this.redPoints = input)}
                    placeholder="with a placeholder"
                >
                    {range(0, 16).map(this.renderInputOption)}
                </Input>
                <Button style={{ width: "60%" }} onClick={this.balanceTeams}>
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

AddMatchComponent.propTypes = {};
