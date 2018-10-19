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
      addingMatch: false,
      loadingOdds: false,
      loadingOddsError: null,
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
      },
      popoverOpen: false
    };

    this.balanceTeams = this.balanceTeams.bind(this);
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

    ["red-defense", "red-offense", "blue-defense", "blue-offense"].forEach(
      circleName => {
        const onClickHandler = () => {
          flashHandle(circleName);
          this.setState({
            popoverOpen: true,
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

          this.removeHandleAnimation(
            this.state.previousSelectedTableHandleName
          );
        };
        const circle = d3.select(`ellipse#${circleName}`);
        const circleText = d3.select(`text#${circleName}`);
        circle.on("click", onClickHandler);
        circleText.on("click", onClickHandler);
      }
    );
  }

  removeHandleAnimation = handleName => {
    d3.select(`g#${handleName}`)
      .attr("opacity", 1)
      .interrupt();
  };

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
        this.updatePlayerDisplay(response.optimal_team_composition);
      },
      () => {
        this.setState({
          analyzePlayersFail: true
        });
      }
    );
  };

  updatePlayerDisplay = playerSetup => {
    d3.select("text#red-defense").text(
      playerSetup.red.defense[0].toUpperCase()
    );
    d3.select("text#red-defense-sm").text(playerSetup.red.defense);
    d3.select("text#red-offense").text(
      playerSetup.red.offense[0].toUpperCase()
    );
    d3.select("text#red-offense-sm").text(playerSetup.red.offense);
    d3.select("text#blue-defense").text(
      playerSetup.blue.defense[0].toUpperCase()
    );
    d3.select("text#blue-defense-sm").text(playerSetup.blue.defense);
    d3.select("text#blue-offense").text(
      playerSetup.blue.offense[0].toUpperCase()
    );
    d3.select("text#blue-offense-sm").text(playerSetup.blue.offense);
  };

  createMatch = (bluePoints, redPoints) => {
    this.setState({ addingMatch: true });
    return postMatch(this.state.selectedPlayers, {
      blue: bluePoints,
      red: redPoints
    }).then(
      () => {
        this.setState({
          analysis: null,
          addingMatch: false
        });
      },
      () => {
        this.setState({
          addingMatch: false
        });
      }
    );
  };

  playersComplete = playersObj => {
    const flatPlayers = new Set([
      ...Object.values(playersObj.red).filter(val => val),
      ...Object.values(playersObj.blue).filter(val => val)
    ]);
    return flatPlayers.size === 4;
  };

  selectPlayer = (color, position, name) => {
    const playersCopy = { ...this.state.selectedPlayers };
    playersCopy[color][position] = name;
    d3.select(`text#${this.state.selectedTableHandleName}`).text(
      name[0].toUpperCase()
    );
    d3.select(`text#${this.state.selectedTableHandleName}-sm`).text(name);
    this.closePopOver();
    if (this.playersComplete(playersCopy)) {
      this.setState({ selectedPlayers: playersCopy, loadingOdds: true }, () => {
        // TODO: move to componentDidUpdate instead
        postTeamAnalysis(playersCopy).then(
          response => {
            this.setState({
              loadingOdds: false,
              predicted_win_prob_for_blue: response.predicted_win_prob_for_blue
            });
          },
          () => {
            this.setState({
              loadingOdds: false,
              loadingOddsError: "Something went wrong"
            });
          }
        );
      });
    } else {
      this.setState({ selectedPlayers: playersCopy });
    }
  };

  selectedPlayersAsList = () => {
    const p = this.state.selectedPlayers;
    return [
      p.blue.offense,
      p.blue.defense,
      p.red.offense,
      p.red.defense
    ].filter(n => n);
  };

  playerRows = (color, position) => {
    const selectedList = this.selectedPlayersAsList();
    return (
      <ListGroup flush>
        {this.state.players
          .filter(name => !selectedList.includes(name))
          .map(name => (
            <ListGroupItem
              key={name}
              tag="button"
              action
              onClick={() => this.selectPlayer(color, position, name)}
            >
              <div
                style={{
                  fontSize: "2em",
                  float: "left",
                  height: 50,
                  width: 50,
                  backgroundColor: "rgb(235,235,235)",
                  textAlign: "center",
                  borderRadius: 50,
                  marginRight: ".2em"
                }}
              >
                {name[0].toUpperCase()}
              </div>
              <div style={{ fontSize: "2em" }}>{name}</div>
            </ListGroupItem>
          ))}
      </ListGroup>
    );
  };

  closePopOver = () => {
    this.setState({ popoverOpen: false });
    this.removeHandleAnimation(this.state.selectedTableHandleName);
  };

  render() {
    const {
      loadingOdds,
      loadingOddsError,
      predicted_win_prob_for_blue,
      addingMatch
    } = this.state;
    return (
      <Container className="text-center">
        {!!this.state.selectedTableHandle && (
          <Popover
            placement="bottom"
            isOpen={this.state.popoverOpen}
            target={this.state.selectedTableHandle}
            style={{ width: "15em" }}
            toggle={this.closePopOver}
          >
            <PopoverHeader>
              <div className="text-center">Players</div>
            </PopoverHeader>
            <PopoverBody style={{ paddingLeft: 0, paddingRight: 0 }}>
              <div
                style={{
                  maxHeight: "30em",
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
        )}
        <Row>
          <Col>
            <AddMatchComponent
              onAddMatch={this.createMatch}
              canAddMatch={this.playersComplete(this.state.selectedPlayers)}
              addingMatch={addingMatch}
            />
          </Col>
        </Row>
        <Row>
          <TableSVG style={{ height: "60vh" }} />
        </Row>

        {(loadingOdds || loadingOddsError || predicted_win_prob_for_blue) && (
          <Row style={{ margin: "2em" }}>
            <Col>
              <GetOddsAndBalanceComponent
                blue={predicted_win_prob_for_blue}
                red={1 - predicted_win_prob_for_blue}
                loadingOdds={loadingOdds}
                loadingOddsError={loadingOddsError}
                onGetBalance={this.balanceTeams}
              />
            </Col>
          </Row>
        )}
      </Container>
    );
  }
}

export default AddMatchForm;
