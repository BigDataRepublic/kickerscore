import React, { Component } from "react";
import axios from "axios";
import { Table } from "reactstrap";
import { Container, Row, Col } from "reactstrap";

class Home extends Component {
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
    this.setState({ players: data });
  }

  getTableRows(position) {
    {
      return this.state.players
        .sort((a, b) => a[`rank_${position}`] - b[`rank_${position}`])
        .map((player, i) => {
          return (
            <tr key={i}>
              <td>{player[`rank_${position}`]}</td>
              <td>{player.username}</td>
              <td>{Math.round(player.current_trueskill[`${position}`])}</td>
            </tr>
          );
        });
    }
  }

  capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  render() {
    const positions = ["overall", "offense", "defense"];
    return (
      <Container>
        <Row>
          <Col>
            <h1>Leaderboard</h1>
          </Col>
        </Row>
        <Row>
          {positions.map(position => {
            return (
              <Col>
                <h2>{this.capitalize(position)}</h2>
                <Table bordered>
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Name</th>
                      <th>TrueSkill</th>
                    </tr>
                  </thead>
                  <tbody>{this.getTableRows(position)}</tbody>
                </Table>
              </Col>
            );
          })}
        </Row>
      </Container>
    );
  }
}

export default Home;
