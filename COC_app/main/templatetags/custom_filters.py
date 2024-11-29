# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def replace_space_with_underscore(value):
    return value.replace(" ", "_")

@register.filter
def get_max_level_previous_TH(hero, town_hall):
    if hero == "Barbarian King":
        th_level = {7: 0, 8: 10, 9:20, 10:30, 11:40, 12:50, 13:65, 14:75, 15:80, 16:90, 17:95}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Archer Queen":
        th_level = {8: 0, 9:10, 10:30, 11:40, 12:50, 13:65, 14:75, 15:80, 16:90, 17:95}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Minion Prince":
        th_level = {9:0, 10:10, 11:20, 12:30, 13:40, 14:50, 15:60, 16:70, 17:80}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Grand Warden":
        th_level = {11:0, 12:20, 13:40, 14:50, 15:55, 16:65, 17:70}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Royal Champion":
        th_level = {13:0, 14:25, 15:30, 16:40, 17:45}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Battle Machine":
        th_level = {5:0, 6:5, 7:10, 8:20, 9:25, 10:30, 11:35}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Battle Copter":
        th_level = {8:15, 9:25, 10:30, 11:35}
        return th_level.get(town_hall, 0)  # Default value is 0 if town_hall is not 10, 11, or 12


@register.filter
def get_max_level_current_TH(hero, town_hall):
    if hero == "Barbarian King":
        th_level = {7: 0, 8: 10, 9:20, 10:30, 11:40, 12:50, 13:65, 14:75, 15:80, 16:90, 17:95, 18:100}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Archer Queen":
        th_level = {8: 0, 9:10, 10:30, 11:40, 12:50, 13:65, 14:75, 15:80, 16:90, 17:95, 18:100}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Minion Prince":
        th_level = {9:0, 10:10, 11:20, 12:30, 13:40, 14:50, 15:60, 16:70, 17:80, 18:90}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Grand Warden":
        th_level = {11:0, 12:20, 13:40, 14:50, 15:55, 16:65, 17:70, 18:75}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Royal Champion":
        th_level = {13:0, 14:25, 15:30, 16:40, 17:45, 18:50}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Battle Machine":
        th_level = {5:0, 6:5, 7:10, 8:20, 9:25, 10:30, 11:35}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12
    elif hero == "Battle Copter":
        th_level = {8:15, 9:25, 10:30, 11:35}
        return th_level.get(town_hall + 1, 0)  # Default value is 0 if town_hall is not 10, 11, or 12


    return town_hall

@register.filter
def equipment_to_hero(equipment):
    if equipment in ["Barbarian Puppet", "Rage Vial", "Earthquake Boots", "Vampstache", "Giant Gauntlet", "Spiky Ball"]:
        return "Barbarian King"
    elif equipment in ["Archer Puppet", "Invisibility Vial", "Giant Arrow", "Healer Puppet", "Frozen Arrow", "Magic Mirror"]:
        return "Archer Queen"
    elif equipment in ["Henchmen Puppet", "Dark Orb"]:
        return "Minion Prince"
    elif equipment in ["Eternal Tome", "Life Gem", "Rage Gem", "Healing Tome", "Fireball", "Lavaloon Puppet"]:
        return "Grand Warden"
    elif equipment in ["Royal Gem", "Seeking Shield", "Hog Rider Puppet", "Haste Vial", "Rocket Spear"]:
        return "Royal Champion"
    return "New equipment - not yet configured"

@register.filter
def check_in_use(equipment, player):
    # pass
    for hero in player["heroes"]:
        try:
            for hero_equipment in hero["equipment"]:
                if equipment == hero_equipment["name"]:
                    return "Yes"
        except KeyError:
            pass
    return "No"

@register.filter
def not_in(value, arg):
    return value not in arg.split(',')

@register.filter
def does_not_start_with(value, arg):
    """Returns True if the value does not start with the provided argument."""
    return not value.startswith(arg)

@register.filter
def is_in_list(value, arg):
    """Returns True if the value is in the provided list."""
    return value in arg

@register.filter
def filter_from_lassi(troops):
    # Start filtering from "L.A.S.S.I"
    start = False
    filtered_troops = []
    for troop in troops:
        if troop['name'] == "L.A.S.S.I":
            start = True
        if start:
            filtered_troops.append(troop)
    return filtered_troops

@register.filter
def filter_until_lassi(troops):
    # Start collecting troops up until "L.A.S.S.I"
    stop = False
    filtered_troops = []
    for troop in troops:
        if troop['name'] == "L.A.S.S.I":
            stop = True
            break  # Stop before adding "L.A.S.S.I"
        filtered_troops.append(troop)
    return filtered_troops