from db import db
from datetime import datetime


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    blue_offense_player = db.Column(db.String(32), db.ForeignKey('player.username'))
    blue_defense_player = db.Column(db.String(32), db.ForeignKey('player.username'))

    red_offense_player = db.Column(db.String(32), db.ForeignKey('player.username'))
    red_defense_player = db.Column(db.String(32), db.ForeignKey('player.username'))

    blue_points = db.Column(db.Integer)
    red_points = db.Column(db.Integer)

    predicted_win_prob_for_blue = db.Column(db.Float)
    match_balance = db.Column(db.Float)


class Player(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    rating_mu = db.Column(db.Float, nullable=False)
    rating_sigma = db.Column(db.Float, nullable=False)

    rating_mu_offense = db.Column(db.Float, nullable=False)
    rating_sigma_offense = db.Column(db.Float, nullable=False)

    rating_mu_defense = db.Column(db.Float, nullable=False)
    rating_sigma_defense = db.Column(db.Float, nullable=False)
