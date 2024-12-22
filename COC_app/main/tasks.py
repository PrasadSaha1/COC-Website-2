from celery import shared_task, group
import logging
from datetime import datetime
from .models import GlobalPlayer, PlayerMonthlyData
from .api import clean_tag, get_all_player_data
import time

# UPS = update_player_history

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

        town_hall_level = player_data.get("townHallLevel", 0)
        builder_hall_level = player_data.get("builderHallLevel", 0)

        clan_name = player_data.get("clan", {}).get("name", "N/A")
        clan_tag = player_data.get("clan", {}).get("tag", "N/A")

        # trophies, XP level, war wins, combined Home Village Troop/Spell/Siege Machine Level, combined Builder Base Troop Level, combined Pet Level, combined Equipment Level 


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
            month=current_time.strftime('%B'),
            year=current_time.year,
            town_hall_level=town_hall_level,
            builder_hall_level=builder_hall_level,
            clan_name=clan_name,
            clan_tag=clan_tag,
            hour=current_time.hour,
            minute=current_time.minute,
            second=current_time.second,
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
    
