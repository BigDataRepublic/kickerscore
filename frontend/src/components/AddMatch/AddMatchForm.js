import React, { Component } from "react";
import { Button, Form, FormGroup, Label, Input, Col, Media, Container, Row, Alert } from "reactstrap";
import axios from "axios";
import FoosballTablePicture from "./foosball_table.png";
import rangeInclusive from "range-inclusive";

let imgStyle = {
  maxHeight: '325px',
  maxWidth: '325px'
};

class AddMatchForm extends Component {
  constructor() {
    super();
    this.state = {
        matchSuccess: false,
        matchFail: false,
        analyzePlayersSuccess: false,
        analyzePlayersFail: false,
        analyzeTeamsSuccess: false,
        analyzeTeamsFail: false,
        players: [],
        predicted_win_prob_for_blue: null,
    };

    this.reset = this.reset.bind(this);
    this.getSelectRows = this.getSelectRows.bind(this);
    this.balanceTeams = this.balanceTeams.bind(this);
    this.getOdds = this.getOdds.bind(this);
  }

  async componentWillMount() {
    const { data } = await axios.get(
      "/kickerscore/api/v1/players"
    );
    this.setState({ players: data
            .sort((a, b) => ('' + a.username).localeCompare(b.username))
            .map(player => {
              return player.username;
            })
    });
  }

  reset() {
    this.setState({
      matchSuccess: false,
      matchFail: false,
      analyzePlayersSuccess: false,
      analyzePlayersFail: false,
      analyzeTeamsSuccess: false,
      analyzeTeamsFail: false
    });
  }

  async getOdds() {
    this.reset();
    const analyzeTeams = {
        players: {
            blue: {
                offense: this.blueOffense.value,
                defense: this.blueDefense.value,
            },
            red: {
                offense: this.redOffense.value,
                defense: this.redDefense.value,
            }
        }
    };

    const self = this;
    await axios
      .post("/kickerscore/api/v1/analyze-teams", analyzeTeams)
      .then(function (response) {
        self.setState({
          analyzeTeamsSuccess: true,
          predicted_win_prob_for_blue: response.data.predicted_win_prob_for_blue
        });
      })
      .catch(function () {
        self.setState({
          analyzeTeamsFail: true
        });
      });
  }

  async balanceTeams() {
    this.reset();
    const analyzePlayers = {
      players: [
        this.blueOffense.value,
        this.redOffense.value,
        this.blueDefense.value,
        this.redDefense.value
      ]
    };

    const self = this;
    await axios
      .post("/kickerscore/api/v1/analyze-players", analyzePlayers)
      .then(function (response) {
        self.setState({
          analyzePlayersSuccess: true,
          predicted_win_prob_for_blue: response.data.predicted_win_prob_for_blue
        });
        self.blueOffense.value = response.data.optimal_team_composition.blue.offense;
        self.redOffense.value = response.data.optimal_team_composition.red.offense;
        self.blueDefense.value = response.data.optimal_team_composition.blue.defense;
        self.redDefense.value = response.data.optimal_team_composition.red.defense;
      })
      .catch(function () {
        self.setState({
          analyzePlayersFail: true
        });
      });
  }

  async createMatch(e) {
    e.preventDefault();
    this.reset();
    const match = {
      players: {
        blue: {
          offense: this.blueOffense.value,
          defense: this.blueDefense.value,
        },
        red: {
          offense: this.redOffense.value,
          defense: this.redDefense.value,
        }
      },
      points: {
        blue: this.bluePoints.value,
        red: this.redPoints.value
      }
    };
    const self = this;
    await axios
      .post("/kickerscore/api/v1/match", match)
      .then(function () {
        self.setState({
          matchSuccess: true,
          analysis: null
        });
        self.createMatchForm.reset();
      })
      .catch(function () {
        self.setState({
          matchFail: true
        });
      });
  }

  getSelectRows() {
      return [''].concat(this.state.players)
        .map((player, i) => {
          return (
            <option key={i}>{player}</option>
          );
        });
  }

  getPointRange() {
      return [''].concat(rangeInclusive(0,20,1))
        .map((player, i) => {
          return (
            <option key={i}>{player}</option>
          );
        });
  }

  render() {
    return (
      <Container>
        <Row>
          <Form
            innerRef={form => (this.createMatchForm = form)}
            onSubmit={e => this.createMatch(e)}
          >
            <FormGroup>
              <Row>
              <Col>
              <Row>
                <Col></Col>
                <Col>
                  <h2>Points</h2>
                  <Row>
                    <Col>
                      <Input
                        type="select"
                        name="redPoints"
                        innerRef={input => (this.redPoints = input)}
                        placeholder="with a placeholder"
                      >
                        {this.getPointRange()}
                      </Input>
                    </Col>
                      <h2>-</h2>
                    <Col>
                      <Input
                        type="select"
                        name="bluePoints"
                        innerRef={input => (this.bluePoints = input)}
                        placeholder="with a placeholder"
                      >
                          {this.getPointRange()}
                      </Input>
                    </Col>
                  </Row>
                </Col>
                <Col></Col>
              </Row>
              <Row>
                <Col>
                  <h2>Red</h2>
                  <Label>Defense:</Label>
                  <Input
                    type="select"
                    name="redDefense"
                    innerRef={input => (this.redDefense = input)}
                    placeholder="with a placeholder">
                      {this.getSelectRows()}
                  </Input>
                  <Label>Offense:</Label>
                  <Input
                    type="select"
                    name="redOffense"
                    innerRef={input => (this.redOffense = input)}
                    placeholder="with a placeholder">
                      {this.getSelectRows()}
                  </Input>
                </Col>
                <Col>
                  <Media left>
            <Media style={imgStyle} object src={ FoosballTablePicture } alt="My PlaceHolder Picture" />
          </Media>
                </Col>
                <Col>
                  <h2>Blue</h2>
                  <Label>Offense:</Label>
                  <Input
                    type="select"
                    name="blueOffense"
                    innerRef={input => (this.blueOffense = input)}
                    placeholder="with a placeholder">
                      {this.getSelectRows()}
                  </Input>
                  <Label>Defense:</Label>
                  <Input
                    type="select"
                    name="blueDefense"
                    innerRef={input => (this.blueDefense = input)}
                    placeholder="with a placeholder">
                      {this.getSelectRows()}
                  </Input>
                </Col>
              </Row>
              <div>
                  {this.state.predicted_win_prob_for_blue ?
                <Container>
                    <Row>
                  <Col />
                  <Col>
                    <h2>Odds</h2>
                  </Col>
                  <Col />
                </Row>
                <Row>
                  <Col />
                  <Col>
                    <h3>{100 - Math.round(this.state.predicted_win_prob_for_blue * 100)} - {Math.round(this.state.predicted_win_prob_for_blue * 100)}</h3>
                  </Col>
                  <Col />
                </Row>
                </Container>
                      : null}
              </div>
              </Col>
              <Row>
                <Col style={{marginLeft: '20px'}}>
                    <Row>
                  <Button onClick={this.balanceTeams}>Balance Teams → </Button>
                    </Row>
                    <Row style={{marginTop: '20px'}}>
                  <Button onClick={this.getOdds}>Compute Odds → </Button>
                    </Row>
                    <Row style={{marginTop: '20px'}}>
                  <Button type="submit">Add Match → </Button>
                    </Row>
                </Col>
              </Row>
              </Row>
            </FormGroup>
          </Form>
        </Row>
        <div onClick={this.reset}>
          {this.state.matchSuccess ? <Row><Alert color="success">Match Added</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.matchFail ? <Row><Alert color="danger">Something went wrong</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.analyzePlayersSuccess ? <Row><Alert color="success">Teams Balanced</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.analyzePlayersFail ? <Row><Alert color="danger">Something went wrong</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.analyzeTeamsSuccess ? <Row><Alert color="success">Odds Computed</Alert></Row> : null}
        </div>
        <div onClick={this.reset}>
          {this.state.analyzeTeamsFail ? <Row><Alert color="danger">Something went wrong</Alert></Row> : null}
        </div>
      </Container>
    );
  }
}

export default AddMatchForm;
