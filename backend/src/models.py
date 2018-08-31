from db import db
from datetime import datetime
from sqlalchemy import func, desc


class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    blue_offense_player = db.Column(db.String(32), db.ForeignKey('player.username'))
    blue_defense_player = db.Column(db.String(32), db.ForeignKey('player.username'))

    red_offense_player = db.Column(db.String(32), db.ForeignKey('player.username'))
    red_defense_player = db.Column(db.String(32), db.ForeignKey('player.username'))

    blue_offense_player_skill_gain_overall = db.Column(db.Float)
    blue_defense_player_skill_gain_overall = db.Column(db.Float)

    blue_offense_player_skill_gain_offense = db.Column(db.Float)
    blue_defense_player_skill_gain_defense = db.Column(db.Float)

    red_offense_player_skill_gain_overall = db.Column(db.Float) 
    red_defense_player_skill_gain_overall = db.Column(db.Float)

    red_offense_player_skill_gain_offense = db.Column(db.Float)
    red_defense_player_skill_gain_defense = db.Column(db.Float)

    blue_points = db.Column(db.Integer)
    red_points = db.Column(db.Integer)

    predicted_win_prob_for_blue = db.Column(db.Float)
    match_balance = db.Column(db.Float)

    def winner(self):
        return "blue" if self.blue_points > self.red_points else "red"

    def serialize(self):
        return {
            "id": self.id,
            "players": {
                "blue": {
                    "offense": {
                        "name": self.blue_offense_player,
                        "skill_gain_overall": self.blue_offense_player_skill_gain_overall,
                        "skill_gain_offense": self.blue_offense_player_skill_gain_offense
                    },
                    "defense": {
                        "name": self.blue_defense_player,
                        "skill_gain_overall": self.blue_defense_player_skill_gain_overall,
                        "skill_gain_defense": self.blue_defense_player_skill_gain_defense
                    }
                },
                "red": {
                    "offense": {
                        "name": self.red_offense_player,
                        "skill_gain_overall": self.red_offense_player_skill_gain_overall,
                        "skill_gain_offense": self.red_offense_player_skill_gain_offense
                    },
                    "defense": {
                        "name": self.red_defense_player,
                        "skill_gain_overall": self.red_defense_player_skill_gain_overall,
                        "skill_gain_defense": self.red_defense_player_skill_gain_defense
                    }
                }
            },
            "points": {
                "blue": self.blue_points,
                "red": self.red_points
            },
            "predicted_win_prob_for_blue": self.predicted_win_prob_for_blue,
            "match_balance": self.match_balance,
            "winner": self.winner()
        }


class Player(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    registration_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    rating_mu = db.Column(db.Float, nullable=False)
    rating_sigma = db.Column(db.Float, nullable=False)

    rating_mu_offense = db.Column(db.Float, nullable=False)
    rating_sigma_offense = db.Column(db.Float, nullable=False)

    rating_mu_defense = db.Column(db.Float, nullable=False)
    rating_sigma_defense = db.Column(db.Float, nullable=False)

    def serialize(self):
        sub = db.session.query(Player.username, func.row_number().over(order_by=desc(Player.rating_mu)).label('pos')).subquery()
        pos = db.session.query(sub.c.pos).filter(sub.c.username == self.username).scalar() - 1

        sub = db.session.query(Player.username, func.row_number().over(order_by=desc(Player.rating_mu_offense)).label('pos')).subquery()
        pos_offense = db.session.query(sub.c.pos).filter(sub.c.username == self.username).scalar() - 1

        sub = db.session.query(Player.username, func.row_number().over(order_by=desc(Player.rating_mu_defense)).label('pos')).subquery()
        pos_defense = db.session.query(sub.c.pos).filter(sub.c.username == self.username).scalar() - 1

        return {
            "username": self.username,
            "registration_date": str(self.registration_date),
            "current_trueskill": {
                "overall": self.rating_mu,
                "offense": self.rating_mu_offense,
                "defense": self.rating_mu_defense
            },
            "current_uncertainty": {
                "overall": self.rating_sigma,
                "offense": self.rating_sigma_offense,
                "defense": self.rating_sigma_defense
            },
            "rank_overall": pos,
            "rank_offense": pos_offense,
            "rank_defense": pos_defense
        }
