from celery import shared_task, group
import logging
from datetime import datetime, timedelta, date
from .models import GlobalPlayer, PlayerMonthlyData, GlobalClan, ClanWarInformation, ClanMonthlyDataWar, PlayerWarInformation
from .api import clean_tag, get_all_player_data, get_clan_war_information
import time
import pytz

# UPS = update_player_history
timezone = pytz.timezone('America/New_York')  # Replace with your desired time zone

# Set up logging
logger = logging.getLogger(__name__)

@shared_task
def process_tags_batch_UPH(tags):
    for tag in tags:
        try:
            process_single_tag_UPH(tag)
        except Exception as e:
            logger.error(f"Error processing tag {tag}: {e}")

@shared_task
def process_single_tag_UPH(tag):
    try:
        player, created = GlobalPlayer.objects.get_or_create(player_tag=clean_tag(tag))

        current_time = datetime.now()
        player_data = get_all_player_data(tag)

        player_name = player_data.get("name", "N/A")
        town_hall_level = player_data.get("townHallLevel", 0)
        builder_hall_level = player_data.get("builderHallLevel", 0)

        clan_name = player_data.get("clan", {}).get("name", "N/A")
        clan_tag = player_data.get("clan", {}).get("tag", "N/A")
        donations_given = player_data.get("donations", 0)
        donations_recieved = player_data.get("donationsReceived", 0)
        clan_capital_contributions = player_data.get("clanCapitalContributions", 0)

        attack_wins = player_data.get("attackWins", 0)
        defense_wins = player_data.get("defenseWins", 0)

        trophies = player_data.get("trophies", 0)
        builder_base_trophies = player_data.get("builderBaseTrophies", 0)
        war_stars = player_data.get("warStars", 0)
        XP_level = player_data.get("expLevel", 0)

        troop_data = player_data["troops"]
        spell_data = player_data["spells"]
        hero_data = player_data["heroes"]
        equipment_data = player_data["heroEquipment"]

        PlayerMonthlyData.objects.create(
            player=player,
            day=current_time.day,
            month=current_time.month,
            year=current_time.year,
            town_hall_level=town_hall_level,
            builder_hall_level=builder_hall_level,
            player_name=player_name,
            clan_name=clan_name,
            clan_tag=clan_tag,
            donations_given=donations_given,
            donations_recieved=donations_recieved,
            clan_capital_contributions=clan_capital_contributions,
            attack_wins=attack_wins,
            defense_wins=defense_wins,
            hour=current_time.hour,
            minute=current_time.minute,
            trophies=trophies,
            builder_base_trophies=builder_base_trophies,
            war_stars=war_stars,
            XP_level=XP_level,
            troop_data=troop_data,
            spell_data=spell_data,
            hero_data=hero_data,
            equipment_data=equipment_data,
        )

    except Exception as e:
        logger.error(f"Error processing tag {tag}: {e}")
        raise e

@shared_task
def update_player_history():
    tags = GlobalPlayer.objects.values_list('player_tag', flat=True)
    
    # Split tags into chunks of 10
    chunk_size = 10
    tag_chunks = [tags[i:i + chunk_size] for i in range(0, len(tags), chunk_size)]
    
    # Create a group of tasks to process the tags in parallel
    tasks = group(process_tags_batch_UPH.s(chunk) for chunk in tag_chunks)
    
    # Execute the group of tasks asynchronously
    tasks.apply_async()
    

@shared_task
def get_clan_war_status():
    clans = GlobalClan.objects.all()
    for clan in clans:
        clan = clean_tag(str(clan))
        war_info = get_clan_war_information(clan)
        if clan == "2PJY2L8R9":
            scheduled_time = timezone.localize(datetime(2024, 12, 23, 9, 18, 5))
            fetch_war_info.apply_async(
                args=[clan],
                eta=scheduled_time
            )
        elif clan == "229RGJG9Q":
            scheduled_time = timezone.localize(datetime(2024, 12, 23, 9, 18, 40))
            fetch_war_info.apply_async(
                args=[clan],
                eta=scheduled_time
            )

        """
        if not (war_info == {'reason': 'accessDenied'} or war_info["state"] == 'notInWar') :
            target_time = datetime.strptime(war_info["endTime"], "%Y%m%dT%H%M%S.%fZ")
            scheduled_time = target_time - timedelta(seconds=15)

            fetch_war_info.apply_async(
                args=[clan],
                eta=scheduled_time
            )
        """


@shared_task
def fetch_war_info(clan_tag):
    clan_tag = clean_tag(clan_tag)
    war_info = get_clan_war_information(clan_tag)
    clan, created = GlobalClan.objects.get_or_create(clan_tag=clan_tag)
    ClanWarInformation.objects.create(clan=clan, war_info=war_info)

    date_started = war_info["preparationStartTime"]
    converted_date = datetime.strptime(date_started, '%Y%m%dT%H%M%S.000Z').date()

    clan_name = war_info["clan"]["name"]

    for player in war_info["clan"]["members"]:
        player_tag = clean_tag(player["tag"])
        player_info, created = GlobalPlayer.objects.get_or_create(player_tag=player_tag)
        roster_number = player["mapPosition"]

        num_attacks = 0
        num_missed_attacks = 0
        attack_1_stars = 0
        attack_1_destruction = 0
        attack_2_stars = 0
        attack_2_destruction = 0

        try:
            num_attacks = len(player["attacks"])
            attack_1_stars = player["attacks"][0]["stars"]
            attack_1_destruction = player["attacks"][0]["destructionPercentage"]
            num_missed_attacks -= 1
            attack_2_stars = player["attacks"][1]["stars"]
            attack_2_destruction = player["attacks"][1]["destructionPercentage"]
            num_missed_attacks -= 1
        except KeyError:
            pass
        except IndexError:
            pass

        PlayerWarInformation.objects.create(player=player_info, date_started=converted_date, clan_name=clan_name, clan_tag=clan_tag,
                                            roster_number=roster_number, num_attacks=num_attacks, attack_1_stars=attack_1_stars, num_missed_attacks=num_missed_attacks,
                                            attack_1_destruction=attack_1_destruction, attack_2_stars=attack_2_stars, attack_2_destruction=attack_2_destruction)
    

@shared_task
def get_monthly_clan_war_info():
    clans = GlobalClan.objects.all()
    current_date = datetime(2025, 1, 3)
    current_time = datetime.now().strftime('%H:%M:%S')  # this is temporary

    if current_date.month == 1:
        # If it's January, go to December of the previous year
        previous_month = 12
        year = current_date.year - 1
    else:
        # Otherwise, just subtract one month
        previous_month = current_date.month - 1
        year = current_date.year

    # Create a new datetime object for the previous month with the same day (1st of the previous month)
    previous_date = datetime(year, previous_month, 1)

    for clan in clans:
        num_wars = 0
        num_wins = 0
        total_players = 0
        total_stars = 0
        total_destruction = 0

        average_war_size = 0
        average_total_stars = 0
        average_stars_per_player = 0
        average_total_destruction = 0
        win_rate = 0
        percent_attacks_completed = 0

        num_attacks_completed = 0
        num_total_attacks = 0


        for war in reversed(clan.war_information.all()):
            if not (war.war_info == {'reason': 'accessDenied'} or war.war_info.get('state') == 'notInWar') :
                start_time = war.war_info["preparationStartTime"]
                date_obj = datetime.strptime(start_time, "%Y%m%dT%H%M%S.%fZ")

                year = date_obj.year
                month = date_obj.month

                if year == current_date.year and month == current_date.month:
                    continue
                elif (year == previous_date.year and month == previous_date.month):
                    num_wars += 1
                    total_players += len(war.war_info["clan"]["members"])
                    total_stars += war.war_info["clan"]["stars"]
                    total_destruction += war.war_info["clan"]["destructionPercentage"]

                    num_attacks_completed += war.war_info["clan"]["attacks"]
                    num_total_attacks += war.war_info["attacksPerMember"] * total_players

                    clan_stars = war.war_info["clan"]["stars"]
                    clan_destruction = war.war_info["clan"]["destructionPercentage"]
                    opponent_stars = war.war_info["opponent"]["stars"]
                    opponent_destruction = war.war_info["opponent"]["destructionPercentage"]  
                    
                    if clan_stars > opponent_stars or clan_stars == opponent_stars and clan_destruction > opponent_destruction:
                        num_wins += 1
                else:
                    break
            
        try:
            average_war_size = total_players / num_wars
            average_total_stars = total_stars / num_wars
            average_stars_per_player = average_total_stars / average_war_size
            average_total_destruction = total_destruction / num_wars

            win_rate = num_wins / num_wars
            percent_attacks_completed = num_attacks_completed / num_total_attacks
        except ZeroDivisionError:
            pass

        ClanMonthlyDataWar.objects.create(
            clan=clan,  # Match based on the clan
            num_wars=num_wars,
            total_players=total_players,
            total_stars=total_stars,
            total_destruction=total_destruction,
            average_war_size=average_war_size,
            average_total_stars=average_total_stars,
            average_stars_per_player=average_stars_per_player,
            average_total_destruction=average_total_destruction,
            month_year=previous_date,
            percent_attacks_completed=percent_attacks_completed,
            win_rate=win_rate,
            current_time=current_time
        )



