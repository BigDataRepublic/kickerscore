from .analysis import *
from .models import Player, MatchParticipant, Match
from .db import db
from .view_models import MatchListViewModel, MatchInformationViewModel

from flask_restful import Resource, reqparse
import json
from trueskill import Rating, rate
from datetime import datetime


class MatchesResource(Resource):
    def get(self):
        return MatchListViewModel().serialize()


class MatchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)

        args = parser.parse_args()

        match_view_model = MatchInformationViewModel(id=args['id'])

        if not match_view_model.exists():
            return f"Match with id {args['id']} not found", 404

        return match_view_model.serialize(), 200

    def post(self):
        # TODO make compatible with 2 and 3 player setups
        parser = reqparse.RequestParser()
        parser.add_argument('players', type=str)
        parser.add_argument('points', type=str)

        args = parser.parse_args()

        players = json.loads(args['players'].replace("'", "\""))
        points = json.loads(args['points'].replace("'", "\""))

        # Create match and set players and points
        match = Match()

        list_of_players = [
            players["blue"]["offense"], players["blue"]["defense"],
            players["red"]["offense"], players["red"]["defense"]]
        if len(set(list_of_players)) != len(list_of_players):
            # Duplicate players
            return "There are duplicate players in your request", 400

        match.blue_points = int(points['blue'])
        match.red_points = int(points['red'])

        # Scale rating difference with absolute difference in match points
        point_delta = abs(match.blue_points - match.red_points) / 5.

        # Set match balance and predicted win probability
        player_blue_offense = Player.query.filter_by(slack_username=players['blue']['offense']).first()
        player_blue_defense = Player.query.filter_by(slack_username=players['blue']['defense']).first()
        player_red_offense = Player.query.filter_by(slack_username=players['red']['offense']).first()
        player_red_defense = Player.query.filter_by(slack_username=players['red']['defense']).first()

        stats = analyze_teams(player_blue_offense, player_blue_defense, player_red_offense, player_red_defense)

        match.match_balance = stats['match_balance']
        match.predicted_win_prob_for_blue = stats['predicted_win_prob_for_blue']

        match.date = datetime.utcnow()
        db.session.add(match)

        # Calculate new ratings for players (OVERALL)
        player_blue_offense_old_rating_overall = Rating(mu=player_blue_offense.rating_mu, sigma=player_blue_offense.rating_sigma)
        player_blue_defense_old_rating_overall = Rating(mu=player_blue_defense.rating_mu, sigma=player_blue_defense.rating_sigma)
        player_red_offense_old_rating_overall = Rating(mu=player_red_offense.rating_mu, sigma=player_red_offense.rating_sigma)
        player_red_defense_old_rating_overall = Rating(mu=player_red_defense.rating_mu, sigma=player_red_defense.rating_sigma)

        # Update ratings
        blue_team = [player_blue_offense_old_rating_overall, player_blue_defense_old_rating_overall]
        red_team = [player_red_offense_old_rating_overall, player_red_defense_old_rating_overall]

        # Team points are intentionally reverted!
        (player_blue_offense_new_rating_overall, player_blue_defense_new_rating_overall), (player_red_offense_new_rating_overall, player_red_defense_new_rating_overall) = rate([blue_team, red_team], ranks=[match.red_points, match.blue_points])
        player_blue_offense_new_rating_overall = Rating(mu=player_blue_offense_old_rating_overall.mu + (player_blue_offense_new_rating_overall.mu - player_blue_offense_old_rating_overall.mu) * point_delta,
                                                        sigma=player_blue_offense_new_rating_overall.sigma)
        player_blue_defense_new_rating_overall = Rating(mu=player_blue_defense_old_rating_overall.mu + (player_blue_defense_new_rating_overall.mu - player_blue_defense_old_rating_overall.mu) * point_delta,
                                                        sigma=player_blue_defense_new_rating_overall.sigma)
        player_red_offense_new_rating_overall = Rating(mu=player_red_offense_old_rating_overall.mu + (player_red_offense_new_rating_overall.mu - player_red_offense_old_rating_overall.mu) * point_delta,
                                                       sigma=player_red_offense_new_rating_overall.sigma)
        player_red_defense_new_rating_overall = Rating(mu=player_red_defense_old_rating_overall.mu + (player_red_defense_new_rating_overall.mu - player_red_defense_old_rating_overall.mu) * point_delta,
                                                       sigma=player_red_defense_new_rating_overall.sigma)

        # Calculate new ratings for players (OFFENSE/DEFENSE)
        player_blue_offense_old_rating_offense = Rating(mu=player_blue_offense.rating_mu_offense, sigma=player_blue_offense.rating_sigma_offense)
        player_blue_defense_old_rating_defense = Rating(mu=player_blue_defense.rating_mu_defense, sigma=player_blue_defense.rating_sigma_defense)
        player_red_offense_old_rating_offense = Rating(mu=player_red_offense.rating_mu_offense, sigma=player_red_offense.rating_sigma_offense)
        player_red_defense_old_rating_defense = Rating(mu=player_red_defense.rating_mu_defense, sigma=player_red_defense.rating_sigma_defense)

        # Update ratings
        blue_team = [player_blue_offense_old_rating_offense, player_blue_defense_old_rating_defense]
        red_team = [player_red_offense_old_rating_offense, player_red_defense_old_rating_defense]

        # Team points are intentionally reverted!
        (player_blue_offense_new_rating_offense, player_blue_defense_new_rating_defense), (player_red_offense_new_rating_offense, player_red_defense_new_rating_defense) = rate([blue_team, red_team], ranks=[match.red_points, match.blue_points])
        player_blue_offense_new_rating_offense = Rating(mu=player_blue_offense_old_rating_offense.mu + (player_blue_offense_new_rating_offense.mu - player_blue_offense_old_rating_offense.mu) * point_delta,
                                                        sigma=player_blue_offense_new_rating_offense.sigma)
        player_blue_defense_new_rating_defense = Rating(mu=player_blue_defense_old_rating_defense.mu + (player_blue_defense_new_rating_defense.mu - player_blue_defense_old_rating_defense.mu) * point_delta,
                                                        sigma=player_blue_defense_new_rating_defense.sigma)
        player_red_offense_new_rating_offense = Rating(mu=player_red_offense_old_rating_offense.mu + (player_red_offense_new_rating_offense.mu - player_red_offense_old_rating_offense.mu) * point_delta,
                                                       sigma=player_red_offense_new_rating_offense.sigma)
        player_red_defense_new_rating_defense = Rating(mu=player_red_defense_old_rating_defense.mu + (player_red_defense_new_rating_defense.mu - player_red_defense_old_rating_defense.mu) * point_delta,
                                                       sigma=player_red_defense_new_rating_defense.sigma)

        # Create MatchParticipants
        mp_blue_offense = MatchParticipant()
        mp_blue_offense.user_id = player_blue_offense.slack_id
        mp_blue_offense.match_id = match.id
        mp_blue_offense.date = match.date
        mp_blue_offense.team = "blue"
        mp_blue_offense.position = "offense"
        mp_blue_offense.overall_skill_gain = (player_blue_offense_new_rating_overall.mu - 3 * player_blue_offense_new_rating_overall.sigma) - (player_blue_offense_old_rating_overall.mu - 3 * player_blue_offense_old_rating_overall.sigma)
        mp_blue_offense.offense_skill_gain = (player_blue_offense_new_rating_offense.mu - 3 * player_blue_offense_new_rating_offense.sigma) - (player_blue_offense_old_rating_offense.mu - 3 * player_blue_offense_old_rating_offense.sigma)
        mp_blue_offense.defense_skill_gain = 0

        db.session.add(mp_blue_offense)

        mp_blue_defense = MatchParticipant()
        mp_blue_defense.user_id = player_blue_defense.slack_id
        mp_blue_defense.match_id = match.id
        mp_blue_defense.date = match.date
        mp_blue_defense.team = "blue"
        mp_blue_defense.position = "defense"
        mp_blue_defense.overall_skill_gain = (player_blue_defense_new_rating_overall.mu - 3 * player_blue_defense_new_rating_overall.sigma) - (player_blue_defense_old_rating_overall.mu - 3 * player_blue_defense_old_rating_overall.sigma)
        mp_blue_defense.offense_skill_gain = 0
        mp_blue_defense.defense_skill_gain = (player_blue_defense_new_rating_defense.mu - 3 * player_blue_defense_new_rating_defense.sigma) - (player_blue_defense_old_rating_defense.mu - 3 * player_blue_defense_old_rating_defense.sigma)

        db.session.add(mp_blue_defense)

        mp_red_offense = MatchParticipant()
        mp_red_offense.user_id = player_red_offense.slack_id
        mp_red_offense.match_id = match.id
        mp_red_offense.date = match.date
        mp_red_offense.team = "red"
        mp_red_offense.position = "offense"
        mp_red_offense.overall_skill_gain = (player_red_offense_new_rating_overall.mu - 3 * player_red_offense_new_rating_overall.sigma) - (player_red_offense_old_rating_overall.mu - 3 * player_red_offense_old_rating_overall.sigma)
        mp_red_offense.offense_skill_gain = (player_red_offense_new_rating_offense.mu - 3 * player_red_offense_new_rating_offense.sigma) - (player_red_offense_old_rating_offense.mu - 3 * player_red_offense_old_rating_offense.sigma)
        mp_red_offense.defense_skill_gain = 0

        db.session.add(mp_red_offense)

        mp_red_defense = MatchParticipant()
        mp_red_defense.user_id = player_red_defense.slack_id
        mp_red_defense.match_id = match.id
        mp_red_defense.date = match.date
        mp_red_defense.team = "red"
        mp_red_defense.position = "defense"
        mp_red_defense.overall_skill_gain = (player_red_defense_new_rating_overall.mu - 3 * player_red_defense_new_rating_overall.sigma) - (player_red_defense_old_rating_overall.mu - 3 * player_red_defense_old_rating_overall.sigma)
        mp_red_defense.offense_skill_gain = 0
        mp_red_defense.defense_skill_gain = (player_red_defense_new_rating_defense.mu - 3 * player_red_defense_new_rating_defense.sigma) - (player_red_defense_old_rating_defense.mu - 3 * player_red_defense_old_rating_defense.sigma)

        db.session.add(mp_red_defense)
        match.participants.append(mp_blue_offense)
        match.participants.append(mp_blue_defense)
        match.participants.append(mp_red_offense)
        match.participants.append(mp_red_defense)

        # Prepare player updates
        player_blue_offense.rating_mu = player_blue_offense_new_rating_overall.mu
        player_blue_offense.rating_sigma = player_blue_offense_new_rating_overall.sigma
        player_blue_defense.rating_mu = player_blue_defense_new_rating_overall.mu
        player_blue_defense.rating_sigma = player_blue_defense_new_rating_overall.sigma

        player_red_offense.rating_mu = player_red_offense_new_rating_overall.mu
        player_red_offense.rating_sigma = player_red_offense_new_rating_overall.sigma
        player_red_defense.rating_mu = player_red_defense_new_rating_overall.mu
        player_red_defense.rating_sigma = player_red_defense_new_rating_overall.sigma

        player_blue_offense.rating_mu_offense = player_blue_offense_new_rating_offense.mu
        player_blue_offense.rating_sigma_offense = player_blue_offense_new_rating_offense.sigma
        player_blue_defense.rating_mu_defense = player_blue_defense_new_rating_defense.mu
        player_blue_defense.rating_sigma_defense = player_blue_defense_new_rating_defense.sigma

        player_red_offense.rating_mu_offense = player_red_offense_new_rating_offense.mu
        player_red_offense.rating_sigma_offense = player_red_offense_new_rating_offense.sigma
        player_red_defense.rating_mu_defense = player_red_defense_new_rating_defense.mu
        player_red_defense.rating_sigma_defense = player_red_defense_new_rating_defense.sigma

        # Update database
        db.session.commit()

        return "OK", 200


class AnalyzePlayers(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('players', type=str, action='append')
        parser.add_argument('best_match_only', type=bool)

        args = parser.parse_args()

        players = list(map(lambda x: Player.query.filter_by(slack_username=x).first(), args['players']))
        best_match_only = args['best_match_only']

        stats = analyze_players(players, best_match_only)

        return stats, 200


class AnalyzeTeams(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('players', type=str)

        args = parser.parse_args()

        players = json.loads(args['players'].replace("'", "\""))

        player_blue_offense = Player.query.filter_by(slack_username=players['blue']['offense']).first()
        player_blue_defense = Player.query.filter_by(slack_username=players['blue']['defense']).first()
        player_red_offense = Player.query.filter_by(slack_username=players['red']['offense']).first()
        player_red_defense = Player.query.filter_by(slack_username=players['red']['defense']).first()

        stats = analyze_teams(player_blue_offense, player_blue_defense, player_red_offense, player_red_defense)

        return stats, 200
