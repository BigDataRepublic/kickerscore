import React, { Component } from "react";
import { Table } from "reactstrap";
import { Container, Row, Col } from "reactstrap";
import { getLeaderboard } from "../../ApiClient";

class Home extends Component {
  constructor() {
    super();
    this.state = {
      players: []
    };
  }

  componentDidMount() {
    this.getLeaderboard();
    this.intervalID = setInterval(() => this.getLeaderboard(), 10000);
  }

  componentWillUnmount() {
    clearInterval(this.intervalID);
  }

  async getLeaderboard() {
    const data = await getLeaderboard();
    this.setState({ players: data });
  }

  getTableRows(position) {
    if (this.state.players.length == 0)
      return;

    return this.state.players[`${position}_players`]
      .sort((a, b) => a["current_rank"][`${position}`] - b["current_rank"][`${position}`])
      .map((player, i) => {
        return (
          <tr key={`${position}_${i}`}>
            <td>{player["current_rank"][`${position}`] + 1}</td>
            <td>{player.username}</td>
            <td>{Math.round(player["current_rating"][`${position}`])}</td>
          </tr>
        );
      });
  }

  capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  render() {
    const positions = ["overall", "offense", "defense"];
    return (
      <Container>
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
                      <th>Rating</th>
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
