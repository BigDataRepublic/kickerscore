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
  }

  async componentDidMount() {
    const data = await getPlayers();
    this.setState({
      players: data.players
    });
    console.log(data)

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
          predicted_win_prob_for_blue: response.predicted_win_prob_for_blue,
          selectedPlayers: response.optimal_team_composition
        });
        const playerSetup = response.optimal_team_composition;
        this.updatePlayerDetails(playerSetup.red.offense, "red-offense");
        this.updatePlayerDetails(playerSetup.red.defense, "red-defense");
        this.updatePlayerDetails(playerSetup.blue.offense, "blue-offense");
        this.updatePlayerDetails(playerSetup.blue.defense, "blue-defense");
      },
      () => {
        this.setState({
          analyzePlayersFail: true
        });
      }
    );
  };

  updatePlayerDetails = (playerName, position) => {
    const player = this.state.players.find(p => p.username === playerName);

    d3.select(`image#${position}`)
      .attr("xlink:href", player.avatar)
      .attr("width", 192)
      .attr("height", 192);
    d3.select(`ellipse#${position}`).style("fill", `url(#pattern-${position})`);
    d3.select(`text#${position}-sm`).text(this.shortenPlayerName(playerName));
    d3.select(`text#${position}`).text("");
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

  selectPlayer = (color, position, name, avatarUrl) => {
    const playersCopy = { ...this.state.selectedPlayers };
    playersCopy[color][position] = name;

    this.updatePlayerDetails(name, `${color}-${position}`);
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

  shortenPlayerName = playerName =>
    playerName.length > 12 ? playerName.substring(0, 11) + "..." : playerName;

  playerRows = (color, position) => {
    const selectedList = this.selectedPlayersAsList();
    return (
      <ListGroup flush>
        {this.state.players
          .filter(p => !selectedList.includes(p.username))
          .sort((a, b) => ("" + a.username).localeCompare(b.username))
          .map(player => (
            <ListGroupItem
              key={player.username}
              tag="button"
              action
              onClick={() =>
                this.selectPlayer(
                  color,
                  position,
                  player.username,
                  player.avatar
                )
              }
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
                  marginRight: ".2em",
                  backgroundImage: `url(${player.avatar})`,
                  backgroundSize: "cover"
                }}
              />
              <div style={{ fontSize: "1.5em", marginTop: "10px" }}>
                {this.shortenPlayerName(player.username)}
              </div>
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
            style={{ width: "18em" }}
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
          <TableSVG style={{ height: "60vh", width: "80vw" }} />
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
