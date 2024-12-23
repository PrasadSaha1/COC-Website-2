import requests
from main.models import *
from datetime import datetime

headers = {
    "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjkwOWMxNmU3LTIwOTYtNDEzMy05ODAwLTk4ZjRjOWFlY2NlNCIsImlhdCI6MTczMTE4NTQ5Miwic3ViIjoiZGV2ZWxvcGVyLzYwYjgyNGZhLTBhYjUtZjZhOC04Zjk1LTFkZTY5YTVlYWFlNSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjY3LjgzLjIwMi4xMzAiXSwidHlwZSI6ImNsaWVudCJ9XX0.3P1pnIYig0c_css_lu2GQ7sJ2uICw-7ysoCsZ3l7_vgibkFxRGSNuSjsfp0ghwaAVtqfXKmw9VMGEyfT9JS6lw"
}



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
        
        clan_general_info = get_all_clan_data(clan)
        members = clan_general_info["memberList"]
        clan_name = clan_general_info["name"]
        clan_tag = clean_tag(clan_general_info["tag"])
        
        for member in members:
            num_wars = 0
            num_attacks = 0
            num_missed_attacks = 0
            total_stars = 0
            total_destruction = 0
            average_total_stars = 0
            average_total_destruction = 0


            player_tag = clean_tag(member["tag"])
            player, created = GlobalPlayer.objects.get_or_create(player_tag=player_tag)
            for war in reversed(player.war_information.all()):
                start_time = str(war.date_started)
                year = int(start_time[0:4])
                month = int(start_time[5:7])

                if war.clan_tag == clan_tag:
                    if year == current_date.year and month == current_date.month:
                        continue
                    elif (year == previous_date.year and month == previous_date.month):
                        num_wars += 1
                        num_attacks += war.num_attacks
                        num_missed_attacks += war.num_missed_attacks
                        total_stars += war.attack_1_stars + war.attack_2_stars
                        total_destruction += war.attack_1_destruction + war.attack_2_destruction
                    else:
                        break
            try: 
                average_total_stars = total_stars / num_wars
                average_total_destruction = total_destruction / num_wars
            except ZeroDivisionError:
                pass
            PlayerMonthlyDataWar.objects.create(player=player, clan_name=clan_name, clan_tag=clan_tag, 
                                                current_time=current_time, month_year=previous_date,
                                                num_wars=num_wars, num_attacks=num_attacks, num_missed_attacks=num_missed_attacks,
                                                total_stars=total_stars, total_destruction=total_destruction, average_total_stars=average_total_stars, average_total_destruction=average_total_destruction)


def fetch_war_info(clan_tag):
    war_info = get_clan_war_information(clean_tag(clan_tag))
    clan, created = GlobalClan.objects.get_or_create(clan_tag=clean_tag(clan_tag))
    ClanWarInformation.objects.create(clan=clan, war_info=war_info)

    date_started = war_info["preparationStartTime"]
    converted_date = datetime.strptime(date_started, '%Y%m%dT%H%M%S.000Z').date()

    clan_name = war_info["clan"]["name"]

    for player in war_info["clan"]["members"]:
        player_tag = clean_tag(player["tag"])
        player_info, created = GlobalPlayer.objects.get_or_create(player_tag=player_tag)
        roster_number = player["mapPosition"]

        num_attacks = 0
        num_missed_attacks = 2
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
    


def find_clan_with_tag(clan_tag, information):
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}", headers=headers)
    response_json = response.json()

    information_to_export = []
    for info in information:
        information_to_export.append(response_json[info])
    return information_to_export

def get_clan_badge(clan_tag):
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}", headers=headers)
    response_json = response.json()
    return response_json["badgeUrls"]["medium"]

def clean_tag(tag):
    return tag.replace("#", "").strip().upper()

def get_member_data(clan_tag):
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/members", headers=headers)
    response_json = response.json()
    return response_json

def get_all_clan_data(clan_tag):
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}", headers=headers)
    response_json = response.json()
    return response_json

def get_all_player_data(player_tag):
    response = requests.get(f"https://api.clashofclans.com/v1/players/%23{player_tag}", headers=headers)
    response_json = response.json()
    return response_json

def get_clan_war_information(clan_tag):
    response = requests.get(f"https://api.clashofclans.com/v1/clans/%23{clan_tag}/currentwar", headers=headers)
    response_json = response.json()
    return response_json
