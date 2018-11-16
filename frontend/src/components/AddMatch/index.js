import React, { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import AddMatchForm from "../AddMatch/AddMatchForm";

class AddMatch extends Component {
  constructor() {
    super();
    this.state = {
      players: []
    };
  }

  render() {
    return (
      <Container>
        <Row>
          <Col>
            <AddMatchForm />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default AddMatch;
