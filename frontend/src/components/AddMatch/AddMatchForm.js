import React, { Component } from "react";
import { Button, Form, FormGroup, Label, Input, Col, Media, Container, Row, Alert } from "reactstrap";
import axios from "axios";
import FoosballTablePicture from "./foosball_table.png";

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
        players: [],
        analysis: null
    };

    this.reset = this.reset.bind(this);
    this.getSelectRows = this.getSelectRows.bind(this);
    this.balanceTeams = this.balanceTeams.bind(this);
  }

  async componentWillMount() {
    const { data } = await axios.get(
      "http://" + process.env.REACT_APP_API_HOST + ":" + process.env.REACT_APP_API_PORT + "/kickerscore/api/v1/players"
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
      .post("http://" + process.env.REACT_APP_API_HOST + ":" + process.env.REACT_APP_API_PORT + "/kickerscore/api/v1/analyze-players", analyzePlayers)
      .then(function (response) {
        console.log('then');
        self.setState({
          analyzePlayersSuccess: true,
          analysis: response.data
        });
        self.blueOffense.value = self.state.analysis.optimal_team_composition.blue.offense;
        self.redOffense.value = self.state.analysis.optimal_team_composition.red.offense;
        self.blueDefense.value = self.state.analysis.optimal_team_composition.blue.defense;
        self.redDefense.value = self.state.analysis.optimal_team_composition.red.defense;
      })
      .catch(function () {
        console.log('fail');
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
      .post("http://" + process.env.REACT_APP_API_HOST + ":" + process.env.REACT_APP_API_PORT + "/kickerscore/api/v1/match", match)
      .then(function () {
        self.setState({
          matchSuccess: true,
          analysis: null
        });
      })
      .catch(function () {
        self.setState({
          matchFail: true
        });
      });
    this.createMatchForm.reset();
  }

  getSelectRows() {
      return [''].concat(this.state.players)
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
                        type="text"
                        name="redPoints"
                        innerRef={input => (this.redPoints = input)}
                        placeholder="with a placeholder"
                      />
                    </Col>
                      <h2>-</h2>
                    <Col>
                      <Input
                        type="text"
                        name="bluePoints"
                        innerRef={input => (this.bluePoints = input)}
                        placeholder="with a placeholder"
                      />
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
                  {this.state.analysis ?
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
                    <h3>{100 - Math.round(this.state.analysis.predicted_win_prob_for_blue * 100)} - {Math.round(this.state.analysis.predicted_win_prob_for_blue * 100)}</h3>
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
      </Container>
    );
  }
}

export default AddMatchForm;
