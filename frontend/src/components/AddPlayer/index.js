import React, { Component } from "react";
import { Container, Row, Alert } from "reactstrap";
import AddPlayerForm from "./AddPlayerForm";

class AddPlayer extends Component {
  constructor() {
    this.state = {
      success: false
    }
  }
  render() {
    return (

      <Container>
        <Row>
          <h1>Add Player</h1>
        </Row>
        <Row>
          <AddPlayerForm />
        </Row>
      </Container>
    );
  }
}

export default AddPlayer;
