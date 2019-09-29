const BASE_URL = process.env.REACT_APP_API_URL || "";
const V1_URL = `${BASE_URL}/kickerscore/api/v1`;
const V2_URL = `${BASE_URL}/kickerscore/api/v2`;

const parseJSON = response => response.json();

const checkResponseStatus = response => {
    if (response.status >= 200 && response.status < 300) {
        return response;
    }
    const error = new Error(response.statusText);
    error.response = response;
    error.unauthorized = response.status === 401;
    error.notFound = response.status === 404;
    throw error;
};

export const getPlayers = async () =>
    fetch(`${V2_URL}/players`)
        .then(checkResponseStatus)
        .then(parseJSON);

export const getLeaderboard = async () =>
    fetch(`${V2_URL}/leaderboard`)
        .then(checkResponseStatus)
        .then(parseJSON);

export const postMatch = (playersData, points) =>
    fetch(`${V2_URL}/match`, {
        method: "POST",
        body: JSON.stringify({players: playersData, points}),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(checkResponseStatus)
        .then(parseJSON);

export const postPlayerAnalysis = async playerList =>
    fetch(`${V2_URL}/analyze-players`, {
        method: "POST",
        body: JSON.stringify({players: playerList}),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(checkResponseStatus)
        .then(parseJSON);

export const postTeamAnalysis = async teamComposition =>
    fetch(`${V2_URL}/analyze-teams`, {
        method: "POST",
        body: JSON.stringify({players: teamComposition}),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(checkResponseStatus)
        .then(parseJSON);


export const recognizeFaces = async image =>
    fetch(`${V2_URL}/recognize-faces`, {
        method: "POST",
        body: JSON.stringify({image: image}),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(checkResponseStatus)
        .then(parseJSON);

export const addFaces = async (embeddings, usernames) =>
    fetch(`${V2_URL}/add-faces`, {
        method: "POST",
        body: JSON.stringify({
            embeddings: embeddings,
            usernames: usernames
        }),
        headers: {
            "Content-Type": "application/json"
        }
    })
        .then(checkResponseStatus)
        .then(parseJSON);
