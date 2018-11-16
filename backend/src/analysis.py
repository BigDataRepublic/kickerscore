from trueskill import Rating, quality, rate, TrueSkill
import itertools
import math
from config import *


def win_probability(ts, team1, team2):
    delta_mu = sum(r.mu for r in team1) - sum(r.mu for r in team2)
    sum_sigma = sum(r.sigma ** 2 for r in itertools.chain(team1, team2))
    size = len(team1) + len(team2)
    denom = math.sqrt(size * (ts.beta ** 2) + sum_sigma)
    return ts.cdf(delta_mu / denom)


def analyze_players(players):
    if len(players) < 2 or len(players) > 4:
        return

    ts = TrueSkill(mu=MU, sigma=SIGMA, beta=BETA, tau=TAU, draw_probability=DRAW_PROB)

    possible_positions = itertools.permutations(players, len(players))

    final_composition = []
    final_blue_team = []
    final_red_team = []
    final_match_balance = 0

    for pos in possible_positions:
        if len(pos) == 2:
            blue_team = [Rating(mu=pos[0].rating_mu, sigma=pos[0].rating_sigma)]
            red_team = [Rating(mu=pos[1].rating_mu, sigma=pos[1].rating_sigma)]

        if len(pos) == 3:
            blue_team = [Rating(mu=pos[0].rating_mu, sigma=pos[0].rating_sigma)]
            red_team = [
                Rating(mu=pos[1].rating_mu_offense, sigma=pos[1].rating_sigma_offense),
                Rating(mu=pos[2].rating_mu_defense, sigma=pos[2].rating_sigma_defense)
            ]

        if len(pos) == 4:
            blue_offense = Rating(mu=pos[0].rating_mu_offense, sigma=pos[0].rating_sigma_offense)
            blue_defense = Rating(mu=pos[1].rating_mu_defense, sigma=pos[1].rating_sigma_defense)

            red_offense = Rating(mu=pos[2].rating_mu_offense, sigma=pos[2].rating_sigma_offense)
            red_defense = Rating(mu=pos[3].rating_mu_defense, sigma=pos[3].rating_sigma_defense)

            blue_team = [blue_offense, blue_defense]
            red_team = [red_offense, red_defense]

        match_balance = ts.quality([blue_team, red_team])

        if match_balance > final_match_balance:
            final_match_balance = match_balance
            final_composition = pos
            final_blue_team = blue_team
            final_red_team = red_team

    if len(players) == 2:
        return {
            "optimal_team_composition": {
                "blue": {
                    "offense": final_composition[0].slack_username
                },
                "red": {
                    "offense": final_composition[1].slack_username
                }
            },
            "match_balance": match_balance,
            "predicted_win_prob_for_blue": win_probability(ts, final_blue_team, final_red_team)
        }

    if len(players) == 3:
        return {
            "optimal_team_composition": {
                "blue": {
                    "offense": final_composition[0].slack_username
                },
                "red": {
                    "offense": final_composition[1].slack_username,
                    "defense": final_composition[2].slack_username
                }
            },
            "match_balance": match_balance,
            "predicted_win_prob_for_blue": win_probability(ts, final_blue_team, final_red_team)
        }

    if len(players) == 4:
        return {
            "optimal_team_composition": {
                "blue": {
                    "offense": final_composition[0].slack_username,
                    "defense": final_composition[1].slack_username
                },
                "red": {
                    "offense": final_composition[2].slack_username,
                    "defense": final_composition[3].slack_username
                }
            },
            "match_balance": match_balance,
            "predicted_win_prob_for_blue": win_probability(ts, final_blue_team, final_red_team)
        }


def _build_team(rating1, rating2):
    team = []
    if rating1 is not None:
        team.append(rating1)

    if rating2 is not None:
        team.append(rating2)

    return team


def analyze_teams(player_blue_offense, player_blue_defense, player_red_offense, player_red_defense):
    ts = TrueSkill(mu=MU, sigma=SIGMA, beta=BETA, tau=TAU, draw_probability=DRAW_PROB)

    player_blue_offense_rating = Rating(mu=player_blue_offense.rating_mu,
                                        sigma=player_blue_offense.rating_sigma) if player_blue_offense is not None else None
    player_blue_defense_rating = Rating(mu=player_blue_defense.rating_mu,
                                        sigma=player_blue_defense.rating_sigma) if player_blue_defense is not None else None
    player_red_offense_rating = Rating(mu=player_red_offense.rating_mu,
                                       sigma=player_red_offense.rating_sigma) if player_red_offense is not None else None
    player_red_defense_rating = Rating(mu=player_red_defense.rating_mu,
                                       sigma=player_red_defense.rating_sigma) if player_red_defense is not None else None

    blue_team = _build_team(player_blue_offense_rating, player_blue_defense_rating)
    red_team = _build_team(player_red_offense_rating, player_red_defense_rating)

    match_balance = ts.quality([blue_team, red_team])
    win_prob = win_probability(ts, blue_team, red_team)

    return {"match_balance": match_balance, "predicted_win_prob_for_blue": win_prob}
