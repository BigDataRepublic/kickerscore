from .models import Player, MatchParticipant, Match
from sqlalchemy import func


class LeaderboardViewModel():
    overall_players = []
    offense_players = []
    defense_players = []

    def __init__(self):
        self.overall_players = list(Player.query.filter(Player.active)
                                                .filter(Player.participant_entries.any())
                                                .order_by(Player.leaderboard_rating_overall.desc()))

        self.offense_players = list(Player.query.filter(Player.active)
                                                .filter(Player.participant_entries.any(MatchParticipant.position == "offense"))
                                                .order_by(Player.leaderboard_rating_offense.desc()))

        self.defense_players = list(Player.query.filter(Player.active)
                                                .filter(Player.participant_entries.any(MatchParticipant.position == "defense"))
                                                .order_by(Player.leaderboard_rating_defense.desc()))

        for ix, p in enumerate(self.overall_players):
            p.overall_position = ix

        for ix, p in enumerate(self.offense_players):
            p.offense_position = ix

        for ix, p in enumerate(self.defense_players):
            p.defense_position = ix

    def serialize(self):
        return {
            "overall_players": list(map(lambda x: x.serialize(), self.overall_players)),
            "offense_players": list(map(lambda x: x.serialize(), self.offense_players)),
            "defense_players": list(map(lambda x: x.serialize(), self.defense_players))
        }


class AddMatchPlayerListViewModel():
    players = []

    def __init__(self):
        self.players = Player.query.filter(Player.active)

    def serialize(self):
        return {"players": list(map(lambda x: {"username": x.slack_username, "avatar": x.slack_avatar, "slack_id": x.slack_id}, self.players))}


class PlayerInformationViewModel():
    player = None

    def __init__(self, username):
        self.player = Player.query.filter(func.lower(Player.slack_username) == username).first()

    def exists(self):
        return self.player is not None

    def serialize(self):
        if not self.exists():
            return None

        return {
            "player": self.player.serialize(),
            "rating_over_time": self.player.rating_over_time
        }


class MatchInformationViewModel():
    match = None

    def __init__(self, match_id):
        self.match = Match.query.filter_by(id=match_id).first()

    def exists(self):
        return self.match is not None

    def serialize(self):
        if self.exists():
            return self.match.serialize()

        return None


class MatchListViewModel():
    matches = []

    def __init__(self):
        self.matches = Match.query.all()

    def serialize(self):
        return {"matches": list(map(lambda x: x.serialize(), self.matches))}
