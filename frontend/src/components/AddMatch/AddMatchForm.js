import React, { Component } from "react";
import { Button, Form, FormGroup, Label, Input, Row, Col, Media } from "reactstrap";
import axios from "axios";

class AddMatchForm extends Component {
  async createMatch(e) {
    console.log("hit");
    e.preventDefault();
    const match = {
      players: {
        blue: {
          offense: this.blueOffense.value,
          defense: this.blueDefense.value,
        },
        red: {
          offense: this.redOffense.value,
          defense: this.redDefense.value,
        }
      },
      points: {
        blue: this.bluePoints.value,
        red: this.redPoints.value
      }
    };
    const matchPost = await axios
      .post(`http://localhost:5000/kickerscore/api/v1/match`, match)
      .then()
      .catch();
    this.createMatchForm.reset();
  }

  render() {
    return (
      <Form
        innerRef={form => (this.createMatchForm = form)}
        onSubmit={e => this.createMatch(e)}
      >
        <FormGroup>
          <Row>
            <Col>
              <h2>Red</h2>
              <Label>Defense:</Label>
              <Input
                type="text"
                name="redDefense"
                innerRef={input => (this.redDefense = input)}
                placeholder="with a placeholder"
              />
              <Label>Offense:</Label>
              <Input
                type="text"
                name="redOffense"
                innerRef={input => (this.redOffense = input)}
                placeholder="with a placeholder"
              />
            </Col>
            <Col>
              <h2>Points</h2>
              <Row>
                <Col>
                  <Input
                    type="text"
                    name="redPoints"
                    innerRef={input => (this.redPoints = input)}
                    placeholder="with a placeholder"
                  />
                </Col>
                  <h2>-</h2>
                <Col>
                  <Input
                    type="text"
                    name="bluePoints"
                    innerRef={input => (this.bluePoints = input)}
                    placeholder="with a placeholder"
                  />
                </Col>
              </Row>
            </Col>
            <Col>
              <h2>Blue</h2>
              <Label>Offense:</Label>
              <Input
                type="text"
                name="blueOffense"
                innerRef={input => (this.blueOffense = input)}
                placeholder="with a placeholder"
              />
              <Label>Defense:</Label>
              <Input
                type="text"
                name="blueDefense"
                innerRef={input => (this.blueDefense = input)}
                placeholder="with a placeholder"
              />
            </Col>
          </Row>
          <Button type="submit">Add Match → </Button>
        </FormGroup>
      </Form>
    );
  }
}

export default AddMatchForm;
