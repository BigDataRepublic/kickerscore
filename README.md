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

To deploy on Kubernetes, including a database, service and ingress:
```
kubectl apply -f deployment.yml
```

## Mechanics
For each player, three TrueSkill ratings are recorded: overall, offense and defense.
The overall rating will be updated after every match, while the offense and defense are only updated when the player has played that specific role.
When a new player name is entered, it is automatically added to the database, starting with a rating of 1000.
When a player doesn't play a single game for 14 days, his TrueSkill rating will decay by 1 point per day.
Playing a single game resets the timer and prevents decay for 14 days.

## API endpoints

### Match endpoint

#### GET /kickerscore/api/v1/matches
Returns 100 most recent finished matches in the database.

```
- id: ...
  players:
    blue:
      offense: ...
      defense: ...
    red:
      offense: ...
      defense: ...
  winner: [blue|red|unknown]
  predicted_win_prob_for_blue: ...
  match_balance: ...
  points:
    blue: ...
    red: ...
- ...
- ...
```

#### GET /kickerscore/api/v1/match/[id]
Returns match with the specified id.

Returns:
```
id: ...
players:
  blue:
    offense: ...
    defense: ...
  red:
    offense: ...
    defense: ...
winner: [blue|red|unknown]
predicted_win_prob_for_blue: <probability that blue team will win this match>
match_balance: <measure between 0 and 1 how balanced this match is>
points:
  blue: ...
  red: ...
```
Any of the above attributes can be null if unknown (in case the match is not finished yet or results weren't entered).

#### POST /kickerscore/api/v1/match
Creates match and its outcome and players.
Once this method is called, a match cannot be changed anymore and all players' TrueSkill ratings are updated.

Arguments:

```
players:
  blue:
    offense: ...
    defense: ...
  red:
    offense: ...
    defense: ...
points:
  blue: ...
  red: ...
```

Returns:

```
trueskill:
  <player1_name>:
    offense:
      trueskill: <new trueskill rating>
      trueskill_delta: <trueskill gain due to this match>
    defense:
      trueskill: <new trueskill rating>
      trueskill_delta: <trueskill gain due to this match>
    overall:
      trueskill: <new trueskill rating>
      trueskill_delta: <trueskill gain due to this match>
  <player2_name>:
    ...
  <player3_name>:
    ...
  <player4_name>:
    ...
```

#### GET /kickerscore/api/v1/analyze_players
Analyzes some stats using just the players competing.

Arguments:
```
players:
  - ...
  - ...
  - ...
  - ...
```

Returns:

```
id: ...
optimal_team_composition:
  blue:
    offense: ...
    defense: ...
  red:
    offense: ...
    defense: ...
predicted_win_prob_for_blue: <probability that blue team will win this match given the optimal team composition is used>
match_balance: <measure between 0 and 1 how balanced this match is, given the optimal team composition is used>
```

#### GET /kickerscore/api/v1/analyze_teams
Predicts win chance of blue team and shows match balance.

```
players:
  blue:
    offense: ...
    defense: ...
  red:
    offense: ...
    defense: ...
```

Returns:

```
predicted_win_prob_for_blue: ...
match_balance: ...
```

#### GET /kickerscore/api/v1/players
Shows all player names and their three current TrueSkill ratings.

Returns:
```
- username: ...
  current_trueskills:
    offensive: ...
    defensive: ...
    overall: ...
  daily_trueskill_delta:
    overall: ...
  registration_date: ...
  current_ranking_position: ...
- ...
```

#### GET /kickerscore/api/v1/player/[username]
Shows a player's TrueSkill history.

Returns:
```
username: ...
trueskills:
  offensive:
    - date: ...
      rating: ...
    - ...
  defensive:
    - date: ...
      rating: ...
    - ...
  overall:
    - date: ...
      rating: ...
    - ...
registration_date: ...
current_ranking_position: ...
```
