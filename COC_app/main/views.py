from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User

from main.api import find_clan_with_tag, get_clan_badge, clean_tag, get_member_data, get_all_clan_data, get_all_player_data
from .models import SavedClan, SavedPlayer, GlobalPlayer, PlayerMonthlyData


@login_required(login_url='/register/')
def home(response):
    return render(response, "main/home.html", {})

@login_required
def settings(response):
    return render(response, "main/settings.html", {})


@login_required(login_url='/register/')
def logout_view(request):
    logout(request)
    return redirect("register:create_account")


@login_required(login_url='/register/')
def change_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        password = request.POST.get('password')

        if new_username and password:
            # Check if the username is already taken
            if User.objects.filter(username=new_username).exists():
                return JsonResponse({'status': 'taken'})

            # Check if the provided password is correct
            user = authenticate(request, username=request.user.username, password=password)
            if user is None:
                return JsonResponse({'status': 'incorrect_password'})

            # Change the username and save
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Username successfully changed.')
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'})
    return render(request, 'main/change_username.html')


@login_required(login_url='/register/')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password is correct
        user = authenticate(request, username=request.user.username, password=current_password)
        if user is None:
            return JsonResponse({'status': 'incorrect_password'})

        # Check if the new passwords match
        if new_password != confirm_password:
            return JsonResponse({'status': 'password_mismatch'})

        # Update the password and save the user
        user.set_password(new_password)
        user.save()

        # Keep the user logged in after changing the password
        update_session_auth_hash(request, user)

        messages.success(request, 'Password successfully changed.')
        return JsonResponse({'status': 'success'})

    return render(request, "main/change_password.html", {})

@login_required(login_url='/register/')
def clan_search(request):
    if request.method == "POST":
        search_type = request.POST.get("search_type") 
        if search_type == "clan":
            old_tag = clean_tag(request.POST.get("clan_tag"))
            try:
                clan_name, clan_tag, clan_type, clan_description, clan_members, clan_points = find_clan_with_tag(old_tag, ["name", "tag", "type", "description", "members", "clanPoints"])
                clan_badge = get_clan_badge(old_tag)
                in_database = SavedClan.objects.filter(user=request.user, clan_tag=old_tag).first()
            except KeyError:
                return render(request, "main/clan_search.html", {"error": "clan"})
            return render(request, "main/clan_search.html", {"clan_name": clan_name, "clan_tag": clan_tag, "clan_type": clan_type,
                        "clan_description": clan_description, "clan_members": clan_members, "clan_points": clan_points, "clan_badge": clan_badge, "saved": in_database})
        else:
            tag = clean_tag(request.POST.get("clan_tag"))
            player_data = get_all_player_data(clean_tag(tag))
            in_database = SavedPlayer.objects.filter(user=request.user, player_tag=tag).first()
            if player_data == {'reason': 'notFound'}:
                return render(request, "main/clan_search.html", {"error": "player", "player_data": "error"})
            return render(request, "main/clan_search.html", {"player_data": player_data, "saved": in_database})
    return render(request, "main/clan_search.html")


@login_required(login_url='/register/')
def toggle_save_clan(request, clan_tag):
    saved_clan = SavedClan.objects.filter(user=request.user, clan_tag=clean_tag(clan_tag)).first()
    clan_name = find_clan_with_tag(clean_tag(clan_tag), ["name"])
    saved_clan_count = SavedClan.objects.filter(user=request.user).count()
    change = None

    if saved_clan:
        saved_clan.delete()
        change = "clan_removed"
    elif saved_clan_count < 5:
        SavedClan.objects.create(user=request.user, clan_tag=clean_tag(clan_tag))
        change = "clan_saved"
    else:
        change = "too_many_clans"

    # Get the list of clans to display
    clans_data = []
    for clan in SavedClan.objects.filter(user=request.user):
        clan_info = find_clan_with_tag(clean_tag(clan.clan_tag), ["name", "tag", "type", "description", "members", "clanPoints"])
        clan_badge = get_clan_badge(clean_tag(clan.clan_tag))
        
        # Prepare the data to pass to the template
        clans_data.append({
            'name': clan_info[0],
            'tag': clan_info[1],
            'type': clan_info[2],
            'description': clan_info[3],
            'members': clan_info[4],
            'clan_points': clan_info[5],
            'badge': clan_badge,
        })

    return render(request, "main/my_clans.html", {
        "change": change,
        "clan_name": clan_name[0],
        "clans": clans_data  # Pass the clans data here
    })

@login_required(login_url='/register/')
def toggle_save_player(request, player_tag):
    saved_player = SavedPlayer.objects.filter(user=request.user, player_tag=clean_tag(player_tag)).first()
    player_name = get_all_player_data(clean_tag(player_tag))["name"]
    #print(player_name)
    saved_player_count = SavedPlayer.objects.filter(user=request.user).count()
    change = None

    if saved_player:
        saved_player.delete()
        change = "player_removed"
    elif saved_player_count < 10:
        SavedPlayer.objects.create(user=request.user, player_tag=clean_tag(player_tag))
        change = "player_saved"
    else:
        change = "too_many_players"
    players_data = []

    for player in SavedPlayer.objects.filter(user=request.user):
        data = get_all_player_data(clean_tag(player.player_tag))
        players_data.append(data)

    return render(request, "main/my_players.html", {
        "change": change,
        "player_name": player_name,
        "players": players_data
    })


@login_required(login_url='/register/')
def my_clans(request):
    clans_data = []

    # Iterate through each saved clan for the logged-in user
    for clan in SavedClan.objects.filter(user=request.user):
        clan_info = find_clan_with_tag(clean_tag(clan.clan_tag), ["name", "tag", "type", "description", "members", "clanPoints"])
        clan_badge = get_clan_badge(clean_tag(clan.clan_tag))
        
        # Prepare the data to pass to the template
        clans_data.append({
            'name': clan_info[0],
            'tag': clan_info[1],
            'type': clan_info[2],
            'description': clan_info[3],
            'members': clan_info[4],
            'clan_points': clan_info[5],
            'badge': clan_badge,
        })

    return render(request, "main/my_clans.html", {'clans': clans_data})

@login_required(login_url='/register/')
def view_clan(request, clan_tag, mode):
    member_data = get_member_data(clean_tag(clan_tag))
    clan_data = get_all_clan_data(clean_tag(clan_tag))

    return render(request, "main/view_clan.html", {"member_data": member_data, "clan_tag": clan_tag, "mode": mode, "clan_data": clan_data,})

@login_required(login_url='/register/')
def my_players(request):
    players_data = []
    for player in SavedPlayer.objects.filter(user=request.user):
        data = get_all_player_data(clean_tag(player.player_tag))
        players_data.append(data)

    return render(request, "main/my_players.html", {'players': players_data})

@login_required(login_url='/register/')
def view_player(request, player_tag):
    player = get_all_player_data(clean_tag(player_tag))
    is_being_tracked = GlobalPlayer.objects.filter(player_tag=clean_tag(player_tag)).exists()
    if request.method == "POST" and not is_being_tracked:
        new_player = GlobalPlayer(player_tag=clean_tag(player_tag))
        new_player.save() 
    return render(request, "main/view_player.html", {"player": player, "is_being_tracked": is_being_tracked})


@login_required(login_url='/register/')
def view_player_history(request, player_tag):
    player = get_all_player_data(clean_tag(player_tag))
    player_history = GlobalPlayer.objects.get(player_tag=clean_tag(player_tag))
    monthly_data = player_history.monthly_data.all()  # Reverse lookup using `related_name`
    if not monthly_data.exists():
        monthly_data = "N/A"

    return render(request, "main/view_player_history.html", {"player": player, "monthly_data": monthly_data})

