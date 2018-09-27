# Kickerscore

Kickerscore is an API that provides a way to keep track of scores for kickers/foosball.

* It shows you a ranking of players
* It allows you to enter your scores and team composition and kickerscore will keep track of your TrueSkill rating, both overall and for offensive and defensive roles specifically
* It will show you the team composition for an optimally balanced match
* It predicts the win/loss odds for a match

## Deployment

To deploy using Docker:

```
docker build . --tag kickerscore
docker run -it kickerscore
```

Make sure to have a postgres database running.

To deploy using docker-compose:
```
docker-compose build && docker-compose up
```

To deploy on Kubernetes, including a database, service and ingress:
```
kubectl apply -f deployment.yml
```

## Mechanics
For each player, three TrueSkill ratings are recorded: overall, offense and defense.
The overall rating will be updated after every match, while the offense and defense are only updated when the player has played that specific role.
When a new player name is entered, it is automatically added to the database, starting with a rating of 1000.
When a player doesn't play a single game for 28 days, his TrueSkill rating will decay by 5 points per day.
Playing a single game resets the timer and prevents decay for 28 days.

## API endpoints

### Match endpoint

#### GET /kickerscore/api/v1/matches
Returns 100 most recent finished matches in the database.

```
[
  {
    "id": 0,
    "players": {
      "blue": {
        "offense": {
          "name": "",
          "skill_gain_overall": 10,
          "skill_gain_offense": 10
        },
        "defense": {
          "name": "",
          "skill_gain_overall": 10,
          "skill_gain_defense": 10
        }
      },
      "red": {
        "offense": {
          "name": "",
          "skill_gain_overall": 10,
          "skill_gain_offense": 10
        },
        "defense": {
          "name": "",
          "skill_gain_overall": 10,
          "skill_gain_defense": 10
        }
      }
    },
    "winner": "",
    "predicted_win_prob_for_blue": 0.5,
    "match_balance": 0.5,
    "points": {
      "blue": "",
      "red": ""
    }
  },
  ...
]
```

#### GET /kickerscore/api/v1/match?id=[id]
Returns match with the specified id.

Returns:
```
{
  "id": 0,
  "players": {
    "blue": {
      "offense": {
        "name": "",
        "skill_gain_overall": 10,
        "skill_gain_offense": 10
      },
      "defense": {
        "name": "",
        "skill_gain_overall": 10,
        "skill_gain_defense": 10
      }
    },
    "red": {
      "offense": {
        "name": "",
        "skill_gain_overall": 10,
        "skill_gain_offense": 10
      },
      "defense": {
        "name": "",
        "skill_gain_overall": 10,
        "skill_gain_defense": 10
      }
    }
  },
  "winner": "",
  "predicted_win_prob_for_blue": 0.5,
  "match_balance": 0.5,
  "points": {
    "blue": "",
    "red": ""
  }
}
```
Any of the above attributes can be null if unknown.

#### POST /kickerscore/api/v1/match
Creates match and its outcome and players.
Once this method is called, a match cannot be changed anymore and all players' TrueSkill ratings are permanently updated.

Arguments (ContentType must be `application/json`):

```
{
  "players": {
    "blue": {
      "offense": "",
      "defense": ""
    },
    "red": {
      "offense": "",
      "defense": ""
    }
  },
  "points": {
    "blue": 10,
    "red": 5
  }
}
```

Returns:

```
{
  "players": {
    "blue": {
      "offense": {
        "rating": 1000.0,
        "rating_gain_overall": -30.0,
        "rating_gain_offense": -30.0
      },
      "defense": {
        "rating": 1000.0,
        "rating_gain_overall": -30.0,
        "rating_gain_defense": -30.0
      }
    },
    "red": {
      "offense": {
        "rating": 1000.0,
        "rating_gain_overall": 30.0,
        "rating_gain_offense": 30.0
      },
      "defense": {
        "rating": 1000.0,
        "rating_gain_overall": 30.0,
        "rating_gain_defense": 30.0
      }
    }
  }
}
```

#### POST /kickerscore/api/v1/analyze-players
Analyzes some stats using just the players competing.

Arguments:
```
{
  "players": ["a", "b", "c", "d"]
}
```

Returns:

```
{
  "optimal_team_composition": {
    "blue": {
      "offense": "",
      "defense": ""
    },
    "red": {
      "offense": "",
      "defense": ""
    }
  },
  "predicted_win_prob_for_blue": <probability that blue team will win this match given the optimal team composition is used>,
  "match_balance": <measure between 0 and 1 how balanced this match is, given the optimal team composition is used>
}
```

#### POST /kickerscore/api/v1/analyze-teams
Predicts win chance of blue team and shows match balance.

```
{
  "players": {
    "blue": {
      "offense": "",
      "defense": ""
    },
    "red": {
      "offense": "",
      "defense": ""
    }
  }
}
```

Returns:

```
{
  "predicted_win_prob_for_blue": 0.5,
  "match_balance": 0.5
}
```

#### GET /kickerscore/api/v1/players
Shows all player names and their three current TrueSkill ratings.

Returns:
```
[
  {
    "username": "",
    "registration_date": datetime,
    "current_trueskill": {
      "overall": 1000,
      "offense": 1000,
      "defense": 1000
    },
    "current_uncertainty": {
      "overall": 333.3,
      "offense": 333.3,
      "defense": 333.3
    },
    "rank_overall": 0,
    "rank_offense": 1,
    "rank_defense": 99
  }
]
```

#### GET /kickerscore/api/v1/player?username=[username]
Shows a player's TrueSkill ratings.

Returns:
```
{
  "username": "",
  "registration_date": datetime,
  "current_trueskill": {
    "overall": 1000,
    "offense": 1000,
    "defense": 1000
  },
  "current_uncertainty": {
    "overall": 333.3,
    "offense": 333.3,
    "defense": 333.3
  },
  "rank_overall": 0,
  "rank_offense": 1,
  "rank_defense": 99
}
```

#### POST /kickerscore/api/v1/player
Creates a new player.

Arguments:
```json
{
  "username": ""
}
```

Returns:
```json
"OK"
```