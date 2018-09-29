import React, { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import AddPlayerForm from "./AddPlayerForm";
import TopHeader from "../../shared/components";

class AddPlayer extends Component {
  render() {
    return (
      <Container>
        <Row>
          <Col>
            <TopHeader>Add Player</TopHeader>
          </Col>
        </Row>
        <Row>
            <Col>
          <AddPlayerForm />
            </Col>
        </Row>
      </Container>
    );
  }
}

export default AddPlayer;
