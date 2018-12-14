import os
import logging

from slackclient import SlackClient

from config import MU, SIGMA
from models import Player
from db import db

logger = logging.getLogger(__name__)


slack_oauth_token = os.environ["SLACK_OAUTH_TOKEN"]
try:
    kickerscore_channel_ids = os.environ.get("KICKERSCORE_CHANNEL_ID").split(",")
except AttributeError:
    kickerscore_channel_ids = []
sc = SlackClient(slack_oauth_token)


def sync_new_and_left_channel_members():
    for channel_id in kickerscore_channel_ids:
        _sync_new_and_left_channel_members_per_channel(channel_id)


def _sync_new_and_left_channel_members_per_channel(channel_id):
    logger.info("Running new channel member check for {}".format(channel_id))
    current_slack_members = set(sc.api_call(
        "conversations.members", channel=channel_id)["members"])
    current_db_players = Player.query.all()
    current_db_players_ids = set([p.slack_id for p in current_db_players])
    to_deactivate_players = current_db_players_ids - current_slack_members
    new_players = current_slack_members ^ current_db_players_ids - to_deactivate_players

    logger.info(f"Going to add {new_players} new player(s)")
    for np in new_players:
        player_info = sc.api_call("users.info", user=np)["user"]
        if len(player_info["profile"]["display_name_normalized"]):
            player_name = player_info["profile"]["display_name_normalized"]
        else:
            player_name = player_info["profile"]["real_name_normalized"]
        to_add = Player(
            slack_id=player_info["id"],
            slack_username=player_name,
            slack_avatar=player_info["profile"]["image_192"],
            rating_mu=MU,
            rating_mu_offense=MU,
            rating_mu_defense=MU,
            rating_sigma=SIGMA,
            rating_sigma_offense=SIGMA,
            rating_sigma_defense=SIGMA
        )
        db.session.add(to_add)

    for to_deactivate in to_deactivate_players:
        to_deactivate_instance = next((p for p in current_db_players
                                       if p.slack_id == to_deactivate))
        to_deactivate_instance.active = False

    db.session.commit()


def sync_existing_members_info():
    current_db_players = Player.query.all()
    logger.info(f"Running existing player sync for {len(current_db_players)} players")

    for player in current_db_players:
        slack_info = sc.api_call("users.info", user=player.slack_id)["user"]
        player.with_updated_slack_info(
            username=slack_info["profile"]["display_name_normalized"],
            avatar=slack_info["profile"]["image_192"]
        )

    db.session.commit()
