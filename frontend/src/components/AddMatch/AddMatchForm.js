import React, { Component } from "react";
import {
  Col,
  Container,
  Row,
  Popover,
  PopoverHeader,
  PopoverBody,
  ListGroup,
  ListGroupItem
} from "reactstrap";
import { ReactComponent as TableSVG } from "./table.svg";
import * as d3 from "d3";
import AddMatchComponent from "./AddMatchComponent";
import GetOddsAndBalanceComponent from "./GetOddsAndBalanceComponent";
import {
  getPlayers,
  postMatch,
  postPlayerAnalysis,
  postTeamAnalysis
} from "../../ApiClient";

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
      previousSelectedTableHandle: null,
      selectedTableHandle: null,
      selectedPlayers: {
        red: {
          offense: null,
          defense: null
        },
        blue: {
          offense: null,
          defense: null
        }
      }
    };

    this.reset = this.reset.bind(this);
    this.balanceTeams = this.balanceTeams.bind(this);
    this.getOdds = this.getOdds.bind(this);
  }

  async componentDidMount() {
    const data = await getPlayers();
    this.setState({
      players: data
        .sort((a, b) => ("" + a.username).localeCompare(b.username))
        .map(player => {
          return player.username;
        })
    });

    const flashHandle = handleName => {
      d3.select(`g#${handleName}`)
        .transition()
        .duration(700)
        .attr("opacity", 0.5)
        .transition()
        .duration(700)
        .attr("opacity", 1)
        .on("end", () => flashHandle(handleName));
    };

    const removeHandleAnimation = handleName => {
      d3.select(`g#${handleName}`)
        .attr("opacity", 1)
        .interrupt();
    };

    ["red-defense", "red-offense", "blue-defense", "blue-offense"].forEach(
      circleName => {
        const circle = d3.select(`ellipse#${circleName}`);
        circle.on("click", () => {
          flashHandle(circleName);
          this.setState({
            previousSelectedTableHandleName: this.state.selectedTableHandleName,
            selectedTableHandleName: null,
            selectedTableHandle: null
          });

          if (this.state.previousSelectedTableHandleName !== circleName) {
            this.setState({
              selectedTableHandleName: circleName,
              selectedTableHandle: circle.node()
            });
          }

          removeHandleAnimation(this.state.previousSelectedTableHandleName);
        });
      }
    );
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

  getOdds() {
    postTeamAnalysis(this.state.selectedPlayers).then(
      response => {
        this.setState({
          analyzeTeamsSuccess: true,
          predicted_win_prob_for_blue: response.predicted_win_prob_for_blue
        });
      },
      () => {
        this.setState({
          analyzeTeamsFail: true
        });
      }
    );
  }

  balanceTeams = () => {
    const playerList = [
      ...Object.values(this.state.selectedPlayers.red),
      ...Object.values(this.state.selectedPlayers.blue)
    ];
    postPlayerAnalysis(playerList).then(
      response => {
        this.setState({
          analyzePlayersSuccess: true,
          predicted_win_prob_for_blue: response.predicted_win_prob_for_blue
        });
        // TODO: update team composition with proposed values
        // this.blueOffense.value = response.optimal_team_composition.blue.offense;
        // this.redOffense.value = response.optimal_team_composition.red.offense;
        // this.blueDefense.value = response.optimal_team_composition.blue.defense;
        // this.redDefense.value = response.optimal_team_composition.red.defense;
      },
      () => {
        this.setState({
          analyzePlayersFail: true
        });
      }
    );
  };

  createMatch = () => {
    postMatch(this.state.selectedPlayers, {
      blue: this.bluePoints.value,
      red: this.redPoints.value
    }).then(
      () => {
        this.setState({
          matchSuccess: true,
          analysis: null
        });
      },
      () => {
        this.setState({
          matchFail: true
        });
      }
    );
  };

  selectPlayer = (color, position, name) => {
    const playersCopy = { ...this.state.selectedPlayers };
    playersCopy[color][position] = name;
    this.setState({ selectedPlayers: playersCopy });
  };

  playerRows = (color, position) => (
    <ListGroup flush>
      {this.state.players.map(name => (
        <ListGroupItem
          key={name}
          tag="button"
          action
          onClick={() => this.selectPlayer(color, position, name)}
        >
          <div
            style={{
              float: "left",
              height: 20,
              width: 20,
              backgroundColor: "rgb(235,235,235)",
              textAlign: "center",
              borderRadius: 50,
              marginRight: ".5em"
            }}
          >
            {name[0].toUpperCase()}
          </div>
          {name}
        </ListGroupItem>
      ))}
    </ListGroup>
  );

  render() {
    return (
      <Container className="text-center">
        {!!this.state.selectedTableHandle && (
          <div>
            <Popover
              placement="bottom"
              isOpen
              target={this.state.selectedTableHandle}
            >
              <PopoverHeader>
                <div className="text-center">Players</div>
              </PopoverHeader>
              <PopoverBody style={{ paddingLeft: 0, paddingRight: 0 }}>
                <div
                  style={{
                    maxHeight: 200,
                    maxWidth: 200,
                    overflowY: "auto",
                    padding: "-5px"
                  }}
                >
                  {this.playerRows(
                    ...this.state.selectedTableHandleName.split("-")
                  )}
                </div>
              </PopoverBody>
            </Popover>
          </div>
        )}
        <Row>
          <Col>
            <Row>
              <Col>
                <Row>
                  <AddMatchComponent />
                </Row>
              </Col>
              <TableSVG style={{ height: "50vh" }} />
            </Row>
          </Col>
        </Row>
        <GetOddsAndBalanceComponent />
      </Container>
    );
  }
}

export default AddMatchForm;
