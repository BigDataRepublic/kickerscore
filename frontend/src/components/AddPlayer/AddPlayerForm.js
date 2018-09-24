import React, { Component } from "react";
import { Button, Form, FormGroup, Label, Input, Alert, Row, Container } from "reactstrap";
import axios from "axios";

class AddPlayerForm extends Component {
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

  async createPlayer(e) {
    e.preventDefault();
    const self = this;
    const player = {
      username: this.name.value
    };
    const playerPost = await axios
      .post("http://" + process.env.REACT_APP_API_HOST + ":" + process.env.REACT_APP_API_PORT + "/kickerscore/api/v1/player", player)
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
    this.createPlayerForm.reset();
  }

  render() {
    return (
      <Container>
        <Row>
          <Form
            innerRef={form => (this.createPlayerForm = form)}
            onSubmit={e => this.createPlayer(e)}
          >
            <FormGroup>
              <Label>Name:</Label>
              <Input
                type="text"
                name="name"
                innerRef={input => (this.name = input)}
                placeholder="with a placeholder"
              />
              <Button type="submit">Add Player → </Button>
            </FormGroup>
          </Form>
        </Row>
        <div onClick={this.reset}>
          {this.state.success ? <Row><Alert color="success">Player Added</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.fail ? <Row><Alert color="danger">Something went wrong</Alert></Row> : null}
        </div>
      </Container>
    );
  }
}

export default AddPlayerForm;
