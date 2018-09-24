import React, { Component } from "react";
import { Button, Form, FormGroup, Label, Input, Col, Media, Container, Row, Alert } from "reactstrap";
import axios from "axios";
import FoosballTablePicture from "./foosball_table.png";

class AddMatchForm extends Component {
  constructor() {
    super();
    this.state = {
      success: false,
      fail: false
    };

    this.reset = this.reset.bind(this);
  }

  reset() {
    this.setState({
      success: false,
      fail: false
    });
  }

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
    const self = this;
    const matchPost = await axios
      .post("http://" + process.env.REACT_APP_API_HOST + ":" + process.env.REACT_APP_API_PORT + "/kickerscore/api/v1/match", match)
      .then(function () {
        self.setState({
          success: true
        });
      })
      .catch(function () {
        self.setState({
          fail: true
        });
      });
    this.createMatchForm.reset();
  }

  render() {
    return (
      <Container>
        <Row>
          <Form
            innerRef={form => (this.createMatchForm = form)}
            onSubmit={e => this.createMatch(e)}
          >
            <FormGroup>
              <Row>
                <Col></Col>
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
                <Col></Col>
              </Row>
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
                  <Media left>
            <Media object src={ FoosballTablePicture } alt="My PlaceHolder Picture" />
          </Media>
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
        </Row>
        <div onClick={this.reset}>
          {this.state.success ? <Row><Alert color="success">Match Added</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.fail ? <Row><Alert color="danger">Something went wrong</Alert></Row> : null}
        </div>
      </Container>
    );
  }
}

export default AddMatchForm;
