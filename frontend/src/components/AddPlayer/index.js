import React, { Component } from "react";
import { Container, Row } from "reactstrap";
import AddPlayerForm from "./AddPlayerForm";

class AddPlayer extends Component {
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
