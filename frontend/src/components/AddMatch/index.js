import React, { Component } from "react";
import { Container, Row, Col } from "reactstrap";
import AddMatchForm from "../AddMatch/AddMatchForm";
import axios from "axios";
import TopHeader from "../../helpers";

class AddMatch extends Component {
  constructor() {
    super();
    this.state = {
      players: []
    };
  }

  async componentWillMount() {
    const { data } = await axios.get(
      "http://localhost:5000/kickerscore/api/v1/players"
    );
    this.setState({ players: data.map(player => {
            return player.username;
        })
    });
  }

  render() {
    return (
      <Container>
        <Row>
          <Col>
            <TopHeader>Add Match</TopHeader>
          </Col>
        </Row>
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
