from trueskill import Rating, quality, rate, TrueSkill
import itertools
import math


MU = 1000
SIGMA = 333
BETA = SIGMA / 2
TAU = SIGMA / 100
DRAW_PROB = 0.01


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
                    "offense": final_composition[0].username
                },
                "red": {
                    "offense": final_composition[1].username
                }
            },
            "match_balance": match_balance,
            "predicted_win_prob_for_blue": win_probability(ts, final_blue_team, final_red_team)
        }

    if len(players) == 3:
        return {
            "optimal_team_composition": {
                "blue": {
                    "offense": final_composition[0].username
                },
                "red": {
                    "offense": final_composition[1].username,
                    "defense": final_composition[2].username
                }
            },
            "match_balance": match_balance,
            "predicted_win_prob_for_blue": win_probability(ts, final_blue_team, final_red_team)
        }

    if len(players) == 4:
        return {
            "optimal_team_composition": {
                "blue": {
                    "offense": final_composition[0].username,
                    "defense": final_composition[1].username
                },
                "red": {
                    "offense": final_composition[2].username,
                    "defense": final_composition[3].username
                }
            },
            "match_balance": match_balance,
            "predicted_win_prob_for_blue": win_probability(ts, final_blue_team, final_red_team)
        }
