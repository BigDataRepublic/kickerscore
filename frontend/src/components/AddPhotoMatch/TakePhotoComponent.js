import React, {Component} from "react";
import Camera from 'react-html5-camera-photo';
import 'react-html5-camera-photo/build/css/index.css';
import {getPlayers, recognizeFaces, addFaces} from "../../ApiClient";
import {ListGroup, ListGroupItem, Popover, PopoverBody, PopoverHeader} from "reactstrap";

export default class TakePhotoComponent extends Component {
    state = {
        photoTaken: false,
        popoverOpen: false,
        crops: [],
        players: []
    };

    async componentDidMount() {
        const data = await getPlayers();
        this.setState({
            players: data.players
        });
    }

    closePopOver = () => {
        this.setState({popoverOpen: false});
    };

    playerRows = (index) => {
        // const selectedList = this.selectedPlayersAsList();
        console.log(this.state.players);
        return (
            <ListGroup flush>
                {this.state.players
                    .filter(p => !this.state.crops[index].player || !this.state.crops[index].player.username.includes(p.username))
                    .sort((a, b) => ("" + a.username).localeCompare(b.username))
                    .map(player => (
                        <ListGroupItem
                            key={player.username}
                            tag="button"
                            action
                            onClick={() => {
                                let newCrops = this.state.crops;
                                newCrops[index].player = player;
                                this.setState({
                                    'crops': newCrops
                                });
                                this.closePopOver();
                            }
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
                            <div style={{fontSize: "1.5em", marginTop: "10px"}}>
                                {this.shortenPlayerName(player.username)}
                            </div>
                        </ListGroupItem>
                    ))}
            </ListGroup>
        );
    };

    shortenPlayerName = playerName =>
        playerName.length > 12 ? playerName.substring(0, 11) + "..." : playerName;

    startMatch = () => {
        let embeddings = this.state.crops.map(player => player.embedding);
        let usernames = this.state.crops.map(player => player.player.username);
        addFaces(embeddings, usernames);
        this.props.onComplete(this.state.crops);
    };

    render() {
        return (
            <div>
                {!!this.state.selectedFace && (
                    <Popover
                        placement="bottom"
                        isOpen={this.state.popoverOpen}
                        target={this.state.selectedFace}
                        style={{width: "18em"}}
                        toggle={this.closePopOver}
                    >
                        <PopoverHeader>
                            <div className="text-center">Players</div>
                        </PopoverHeader>
                        <PopoverBody style={{paddingLeft: 0, paddingRight: 0}}>
                            <div
                                style={{
                                    maxHeight: "30em",
                                    overflowY: "auto",
                                    padding: "-5px"
                                }}
                            >
                                {this.playerRows(
                                    this.state.selectedFaceIndex
                                )}
                            </div>
                        </PopoverBody>
                    </Popover>
                )}
                {!this.state.photoTaken &&
                <Camera
                    onTakePhoto={(dataUri) => {
                        let encodedImage = dataUri.substr(22, dataUri.length);

                        recognizeFaces(encodedImage).then((response) => {
                            console.log(response);
                            this.setState({
                                'crops': response.outputs,
                                'photoTaken': true
                            })
                        });
                    }}
                />
                }
                {this.state.photoTaken &&
                <div>
                    <ul>
                        {this.state.crops.map((value, index) => {
                            return <li key={index} style={{'listStyle':'none'}}>
                                <img style={{'height': '150px'}} src={'data:image/png;base64,' + value.image}/>&nbsp;
                                <img style={{'width': '150px', 'height': '150px'}} id={'face' + index} src={value.player ? value.player.avatar : '/user.png'}
                                     onClick={() => {
                                         this.setState({
                                             popoverOpen: true,
                                             selectedFace: 'face' + index,
                                             selectedFaceIndex: index
                                         });
                                     }}/>
                            </li>
                        })}
                    </ul>
                    <button className='btn btn-primary' disabled={ this.state.crops.length !== 4 || this.state.crops.some(p => p.player == null)} onClick={this.startMatch}>Start
                        match
                    </button>&nbsp;
                    <button className='btn btn-danger' onClick={() => this.setState({'photoTaken': false})}>Try again
                    </button>
                </div>
                }
            </div>
        );
    }
}

TakePhotoComponent.propTypes = {};
