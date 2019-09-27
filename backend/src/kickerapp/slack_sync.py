import os
import logging

from slackclient import SlackClient

from .config import MU, SIGMA
from .models import Player
from .db import db


# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


slack_oauth_token = os.environ["SLACK_OAUTH_TOKEN"] if "SLACK_OAUTH_TOKEN" in os.environ else None
try:
    kickerscore_channel_ids = os.environ.get("KICKERSCORE_CHANNEL_ID").split(",")
except AttributeError:
    kickerscore_channel_ids = []
sc = SlackClient(slack_oauth_token)


def sync_new_and_left_channel_members():
    if slack_oauth_token is None:
        logger.warn("SLACK_OAUTH_TOKEN is not defined, cannot do Slack sync")
        return

    if len(kickerscore_channel_ids) == 0:
        logger.warn("KICKERSCORE_CHANNEL_ID is not defined, cannot do Slack sync")
        return

    current_slack_members = []
    for channel_id in kickerscore_channel_ids:
        logger.info("Running new channel member check for {}".format(channel_id))
        channel_users = sc.api_call(
            "conversations.members", channel=channel_id)
        if "members" in channel_users:
            current_slack_members += channel_users["members"]
        else:
            # Error in getting Slack members
            logger.error("Error while retrieving Slack members for channel ID {}".format(channel_id))

    current_slack_members = set(current_slack_members)

    if len(current_slack_members) == 0:
        logger.warn("0 Slack members found while syncing channel members")
        return

    current_db_players = Player.query.all()
    current_db_players_ids = set([p.slack_id for p in current_db_players])
    to_deactivate_players = current_db_players_ids - current_slack_members
    to_reactivate_players = current_db_players_ids.intersection(current_slack_members)

    new_players = current_slack_members ^ current_db_players_ids - to_deactivate_players

    _sync_new_and_left_channel_members_per_channel(new_players, to_deactivate_players, to_reactivate_players)


def _make_username(player_info):
    if "display_name_normalized" in player_info["profile"] and len(player_info["profile"]["display_name_normalized"]) > 0:
        player_name = player_info["profile"]["display_name_normalized"]
    elif "display_name" in player_info["profile"] and len(player_info["profile"]["display_name"]) > 0:
        player_name = player_info["profile"]["display_name"]
    elif "real_name_normalized" in player_info["profile"] and len(player_info["profile"]["real_name_normalized"]) > 0:
        player_name = player_info["profile"]["real_name_normalized"]
    elif "real_name" in player_info["profile"] and len(player_info["profile"]["real_name"]) > 0:
        player_name = player_info["profile"]["real_name"]
    else:
        player_name = player_info["id"]

    return player_name


def _sync_new_and_left_channel_members_per_channel(new_players, to_deactivate_players, to_reactivate_players):
    current_db_players = Player.query.all()
    logger.info(f"Going to add {len(new_players)} new player(s)")
    for np in new_players:
        player_info = sc.api_call("users.info", user=np)["user"]
        player_name = _make_username(player_info)

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

    for to_reactivate in to_reactivate_players:
        to_reactivate_instance = next((p for p in current_db_players
                                       if p.slack_id == to_reactivate))
        to_reactivate_instance.active = True

    db.session.commit()


def sync_existing_members_info():
    if slack_oauth_token is None:
        logger.warn("SLACK_OAUTH_TOKEN is not defined, cannot do Slack sync")
        return

    current_db_players = Player.query.all()
    logger.info(f"Running existing player sync for {len(current_db_players)} players")

    for player in current_db_players:
        slack_info = sc.api_call("users.info", user=player.slack_id)["user"]

        # Determine username
        username = _make_username(slack_info)

        player.with_updated_slack_info(
            username=username,
            avatar=slack_info["profile"]["image_192"]
        )

    db.session.commit()
