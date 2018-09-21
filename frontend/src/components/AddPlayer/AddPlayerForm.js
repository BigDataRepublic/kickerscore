import React, { Component } from "react";
import { Button, Form, FormGroup, Label, Input } from "reactstrap";
import axios from "axios";

class AddPlayerForm extends Component {
  async createPlayer(e) {
    console.log("hit");
    e.preventDefault();
    const player = {
      username: this.name.value
    };
    const playerPost = await axios
      .post(`http://localhost:5000/kickerscore/api/v1/player`, player)
      .then()
      .catch();
    this.createPlayerForm.reset();
  }

  render() {
    return (
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
    );
  }
}

export default AddPlayerForm;
