from flask_restful import Resource, reqparse
from models import Match
import analysis
from models import Player
import json
from trueskill import Rating, rate
from db import db


class MatchesResource(Resource):
    def get(self):
        return list(map(lambda x: x.serialize(), Match.query.limit(100).all())), 200


class MatchResource(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=int)

        args = parser.parse_args()

        match = Match.query.filter_by(id=args['id']).first()

        if match is None:
            return f"AddMatch with id {args['id']} not found", 404

        return match.serialize(), 200

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
        match.blue_offense_player = players['blue']['offense'].lower()
        match.blue_defense_player = players['blue']['defense'].lower()
        match.red_offense_player = players['red']['offense'].lower()
        match.red_defense_player = players['red']['defense'].lower()

        list_of_players = [match.blue_offense_player, match.blue_defense_player, match.red_offense_player, match.red_defense_player]
        if len(set(list_of_players)) != len(list_of_players):
            # Duplicate players
            return "There are duplicate players in your request", 400

        match.blue_points = int(points['blue'])
        match.red_points = int(points['red'])

        # Set match balance and predicted win probability
        player_blue_offense = Player.query.filter_by(username=players['blue']['offense'].lower()).first()
        player_blue_defense = Player.query.filter_by(username=players['blue']['defense'].lower()).first()
        player_red_offense = Player.query.filter_by(username=players['red']['offense'].lower()).first()
        player_red_defense = Player.query.filter_by(username=players['red']['defense'].lower()).first()

        stats = analysis.analyze_teams(player_blue_offense, player_blue_defense, player_red_offense, player_red_defense)

        match.match_balance = stats['match_balance']
        match.predicted_win_prob_for_blue = stats['predicted_win_prob_for_blue']

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

        # Calculate deltas
        match.blue_offense_player_skill_gain_overall = player_blue_offense_new_rating_overall.mu - player_blue_offense_old_rating_overall.mu
        match.blue_defense_player_skill_gain_overall = player_blue_defense_new_rating_overall.mu - player_blue_defense_old_rating_overall.mu
        match.red_offense_player_skill_gain_overall = player_red_offense_new_rating_overall.mu - player_red_offense_old_rating_overall.mu
        match.red_defense_player_skill_gain_overall = player_red_defense_new_rating_overall.mu - player_red_defense_old_rating_overall.mu

        match.blue_offense_player_skill_gain_offense = player_blue_offense_new_rating_offense.mu - player_blue_offense_old_rating_offense.mu
        match.blue_defense_player_skill_gain_defense = player_blue_defense_new_rating_defense.mu - player_blue_defense_old_rating_defense.mu
        match.red_offense_player_skill_gain_offense = player_red_offense_new_rating_offense.mu - player_red_offense_old_rating_offense.mu
        match.red_defense_player_skill_gain_defense = player_red_defense_new_rating_defense.mu - player_red_defense_old_rating_defense.mu

        db.session.add(match)

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

        args = parser.parse_args()

        players = list(map(lambda x: Player.query.filter_by(username=x).first(), args['players']))
        stats = analysis.analyze_players(players)

        return stats, 200


class AnalyzeTeams(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('players', type=str)

        args = parser.parse_args()

        players = json.loads(args['players'].replace("'", "\""))

        player_blue_offense = Player.query.filter_by(username=players['blue']['offense']).first()
        player_blue_defense = Player.query.filter_by(username=players['blue']['defense']).first()
        player_red_offense = Player.query.filter_by(username=players['red']['offense']).first()
        player_red_defense = Player.query.filter_by(username=players['red']['defense']).first()

        stats = analysis.analyze_teams(player_blue_offense, player_blue_defense, player_red_offense, player_red_defense)

        return stats, 200
