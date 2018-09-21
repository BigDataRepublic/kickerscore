import React, { Component } from "react";
import { Container, Row, Alert } from "reactstrap";
import AddMatchForm from "../AddMatch/AddMatchForm";
import axios from "axios";

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
          <h1>Add Match</h1>
        </Row>
        <Row>
          <AddMatchForm />
        </Row>
      </Container>
    );
  }
}

export default AddMatch;
