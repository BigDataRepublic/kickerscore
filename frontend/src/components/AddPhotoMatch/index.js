import React, { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import AddPhotoMatchForm from "../AddPhotoMatch/AddPhotoMatchForm";

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
            <AddPhotoMatchForm />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default AddMatch;
