from .db import db
from .config import *

from datetime import datetime
from sqlalchemy import func, desc
from sqlalchemy.ext.hybrid import hybrid_property
from itertools import accumulate


# Join class
class MatchParticipant(db.Model):
    user_id = db.Column('user_id', db.String(16), db.ForeignKey('player.slack_id'), primary_key=True)
    match_id = db.Column('match_id', db.Integer, db.ForeignKey('match.id'), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    team = db.Column('team', db.String(4))
    position = db.Column('position', db.String(7))

    player = db.relationship('Player', back_populates='participant_entries', lazy='subquery')

    overall_skill_gain = db.Column('overall_skill_gain', db.Float)
    offense_skill_gain = db.Column('offense_skill_gain', db.Float)
    defense_skill_gain = db.Column('defense_skill_gain', db.Float)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.player.slack_username,
            "team": self.team,
            "position": self.position,
            "overall_skill_gain": self.overall_skill_gain,
            "offense_skill_gain": self.offense_skill_gain,
            "defense_skill_gain": self.defense_skill_gain
        }


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    participants = db.relationship('MatchParticipant', lazy='subquery')

    blue_points = db.Column(db.Integer)
    red_points = db.Column(db.Integer)

    predicted_win_prob_for_blue = db.Column(db.Float)
    match_balance = db.Column(db.Float)

    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def winner(self):
        return "blue" if self.blue_points > self.red_points else "red"

    def serialize(self):
        return {
            "id": self.id,
            "players": list(map(lambda x: x.serialize(), self.participants)),
            "points": {
                "blue": self.blue_points,
                "red": self.red_points
            },
            "predicted_win_prob_for_blue": self.predicted_win_prob_for_blue,
            "match_balance": self.match_balance,
            "winner": self.winner()
        }


class Player(db.Model):
    slack_id = db.Column(db.String(16), primary_key=True)
    slack_username = db.Column(db.String(64))
    slack_avatar = db.Column(db.Text)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    active = db.Column(db.Boolean, nullable=False, default=True)

    participant_entries = db.relationship('MatchParticipant', back_populates='player', lazy='select')

    rating_mu = db.Column(db.Float, nullable=False)
    rating_sigma = db.Column(db.Float, nullable=False)

    rating_mu_offense = db.Column(db.Float, nullable=False)
    rating_sigma_offense = db.Column(db.Float, nullable=False)

    rating_mu_defense = db.Column(db.Float, nullable=False)
    rating_sigma_defense = db.Column(db.Float, nullable=False)

    overall_position = None
    offense_position = None
    defense_position = None

    @hybrid_property
    def leaderboard_rating_overall(self):
        return self.rating_mu - 3 * self.rating_sigma

    @hybrid_property
    def leaderboard_rating_offense(self):
        return self.rating_mu_offense - 3 * self.rating_sigma_offense

    @hybrid_property
    def leaderboard_rating_defense(self):
        return self.rating_mu_defense - 3 * self.rating_sigma_defense

    @property
    def rating_over_time(self):
        pe = MatchParticipant.query.filter(MatchParticipant.user_id == self.slack_id).order_by(MatchParticipant.date).with_entities(MatchParticipant.date, MatchParticipant.overall_skill_gain)
        pe = list(pe)

        over_time = list(accumulate(pe, lambda x, y: (y[0], x[1] + y[1])))
        over_time = list(map(lambda x: (str(x[0]), x[1]), over_time))

        return dict(over_time)

    def with_updated_slack_info(self, username: str, avatar: str):
        self.slack_avatar = avatar
        self.slack_username = username
        return self

    def serialize(self):
        return {
            "slack_id": self.slack_id,
            "username": self.slack_username,
            "avatar": self.slack_avatar,
            "registration_date": str(self.registration_date),
            "current_mu": {
                "overall": self.rating_mu,
                "offense": self.rating_mu_offense,
                "defense": self.rating_mu_defense
            },
            "current_sigma": {
                "overall": self.rating_sigma,
                "offense": self.rating_sigma_offense,
                "defense": self.rating_sigma_defense
            },
            "current_rating": {
                "overall": self.leaderboard_rating_overall,
                "offense": self.leaderboard_rating_offense,
                "defense": self.leaderboard_rating_defense
            },
            "current_rank": {
                "overall": self.overall_position,
                "offense": self.offense_position,
                "defense": self.defense_position
            }
        }
