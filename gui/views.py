import random
from django import views
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from gui.forms import RegisterUserForm
from .models import Dragon, Fight, Player
# Create your views here.

@login_required(login_url='/login')
def index(request):
    """Welcome page."""
    context = {
        'dragons': Dragon.objects.filter(owner=request.user)
    }
    return render(request, 'index.html', context)

@login_required(login_url='/login')
def my_sale(request):
    """My sale page"""
    context = {
        'dragons': Dragon.objects.filter(owner=request.user)
    }
    return render(request, 'my_sale.html', context)

@login_required(login_url='/login')
def market(request):
    """Marketplace page"""
    context = {
        'dragons': Dragon.objects.filter(for_sale=True),
        'player': Player.objects.get(user=request.user)
    }
    return render(request, 'market.html', context)

@login_required(login_url='/login')
def remove_from_market(request, dragonId):
    """Remove dragon from market"""
    dragon = Dragon.objects.get(pk=dragonId)
    dragon.for_sale = False
    dragon.save()
    return JsonResponse({'state': 'updated'})

@login_required(login_url='/login')
def add_to_market(request, dragonId, price):
    """Put dragon for selling in the market"""
    dragon = Dragon.objects.get(pk=dragonId)
    dragon.for_sale = True
    dragon.price = price
    dragon.save()
    return JsonResponse({'state': 'updated'})

    
@login_required(login_url='/login')
def buy_dragon(request, dragonId):
    """Put dragon for selling in the market"""
    dragon = Dragon.objects.get(pk=dragonId)
    player = Player.objects.get(user=request.user)
    if player.money > dragon.price:
        player.money -= dragon.price
        dragon.for_sale = False
        dragon.owner = request.user

        dragon.save()
        player.save()
    else:
        print('Problem with buying dragon')

    return JsonResponse({'state': 'updated'})

@login_required(login_url='/login')
def breed(request):
    """Breeding page"""
    context = {
        'dragons': Dragon.objects.filter(owner=request.user)
    }
    return render(request, 'breed.html', context)

@login_required(login_url='/login')
def breed_dragons(request):
    try:
        id1 = request.POST['dragon1']
        id2 = request.POST['dragon2']
        dragon_name = request.POST['dragon_name']
    except KeyError:
        return HttpResponseNotFound('There was problem with received dragon ids for breeding')
    
    if id1 == id2:
        return JsonResponse({'state': 'failed', 'message': 'dragons can not have same id'})

    dragon1 = Dragon.objects.get(pk=id1)
    dragon2 = Dragon.objects.get(pk=id2)
    new_type=1
    
    if dragon1.type == dragon2.type:
        if dragon1.type <= 3:
            new_type=dragon1.type = dragon1.type + 3
        else:
            new_type = 9
    else:
        if dragon1.type <=3 or dragon2.type <=3:
            new_type = random.randint(1, 3)
        else:
            new_type = random.randint(4, 8)

    new_dragon = create_dragon(dragon1, dragon2)
    new_dragon.type = new_type
    new_dragon.owner = request.user
    new_dragon.name = dragon_name
    new_dragon.save()
    player = Player.objects.get(user=request.user)
    player.money = player.money - 30
    player.save()
    return JsonResponse({'state': 'updated'})

def create_dragon(dragon1, dragon2):
    breeded_dragon = Dragon()
    breeded_dragon.attack = generate_stat(dragon1.attack, dragon2.attack)
    breeded_dragon.hp = generate_stat(dragon1.hp, dragon2.hp)
    breeded_dragon.speed = generate_stat(dragon1.speed, dragon2.speed)
    breeded_dragon.defense = generate_stat(dragon1.defense, dragon2.defense)
    breeded_dragon.for_sale = False
    breeded_dragon.price = 0
    return breeded_dragon


def generate_stat(stat1, stat2):
    return (stat1*random.randint(40,60))/100 + (stat2*random.randint(40,60))/100


@login_required(login_url='/login')
def fight_view(request):
    """Fight between the dragons"""
    all_dragons = Dragon.objects.all()

    other_dragons = []
    for dragon in all_dragons:
        if dragon.owner != request.user:
            other_dragons.append(dragon)
    context = {
        'my_dragons': Dragon.objects.filter(owner=request.user),
        'other_dragons': other_dragons
    }
    return render(request, 'fight.html', context)

@login_required(login_url='/login')
def fight(request):
    """Fight between two dragons"""
    player = Player.objects.get(user=request.user)
    try:
        id1 = request.POST['dragon1']
        id2 = request.POST['dragon2']
    except KeyError:
        return HttpResponseNotFound('There was problem with finding dragon ids in request')
    user_dragon = Dragon.objects.get(pk=id1)
    other_dragon = Dragon.objects.get(pk=id2)

    if not validate_if_dragons_can_fight(request.user, user_dragon, other_dragon):
        return JsonResponse({'error': 'There was problem with dragons ownership'})

    fight_result = start_fight(user_dragon, other_dragon)
    fight_result.stolen_money = transfer_stolen_money(fight_result.dragon_winner_owner, fight_result.dragon_loser_owner)
    fight_result.save()
    

    return JsonResponse({
        'winner-owner': fight_result.dragon_winner_owner.username,
        'loser-owner':fight_result.dragon_loser_owner.username, 'state':'finished',
        'winner-name': fight_result.dragon_winner_name,
        'rounds': fight_result.rounds })

def validate_if_dragons_can_fight(user,user_dragon, other_dragon):
    if user == user_dragon.owner and user != other_dragon.owner:
        return True
    return False

def start_fight(user_dragon, other_dragon):
    hp_of_user_dragon = user_dragon.hp
    hp_of_other_dragon = other_dragon.hp
    rounds = 0
    dragon_winner_name = ''
    dragon_loser_name = ''
    while hp_of_other_dragon > 0 and hp_of_other_dragon > 0:
        rounds = rounds + 1
        if user_dragon.speed > other_dragon.speed:
            first_attack = damage(user_dragon.attack, other_dragon.defense)
            hp_of_other_dragon = hp_of_other_dragon - first_attack
            if hp_of_other_dragon <= 0:
                dragon_winner_name = user_dragon.name
                dragon_loser_name= other_dragon.name
                break

            second_attack = damage(other_dragon.attack, user_dragon.defense)
            hp_of_user_dragon = hp_of_user_dragon- second_attack
            if hp_of_user_dragon <= 0:
                dragon_winner_name = other_dragon.name
                dragon_loser_name = user_dragon.name
                break
        else:
            first_attack = damage(other_dragon.attack, user_dragon.defense)
            hp_of_user_dragon = hp_of_user_dragon- first_attack
            if hp_of_user_dragon <= 0:
                dragon_winner_name = other_dragon.name
                dragon_loser_name = user_dragon.name
                break

            second_attack = damage(user_dragon.attack, other_dragon.defense)
            hp_of_other_dragon = hp_of_other_dragon - second_attack
            if hp_of_other_dragon <= 0:
                dragon_winner_name = user_dragon.name
                dragon_loser_name = other_dragon.name
                break
        
    fight_result = Fight()
    fight_result.rounds = rounds
    fight_result.dragon_winner_name = dragon_winner_name
    fight_result.dragon_loser_name = dragon_loser_name
    
    if user_dragon.name == dragon_winner_name:
        fight_result.dragon_winner_owner = user_dragon.owner
        fight_result.dragon_loser_owner = other_dragon.owner
    else:
        fight_result.dragon_winner_owner = other_dragon.owner
        fight_result.dragon_loser_owner = user_dragon.owner
    return fight_result

    

def damage(dragon1_attack, dragon2_defense):
    default_damage = 5
    damage = dragon1_attack - dragon2_defense
    return damage if dragon1_attack > dragon2_defense else default_damage

def transfer_stolen_money(user_to_win_money, user_to_lose_money):
    player_to_win_money = Player.objects.get(user = user_to_win_money)
    player_to_lose_money = Player.objects.get(user = user_to_lose_money)

    stolen_amount = player_to_lose_money.money * 0.05
    player_to_lose_money.money = player_to_lose_money.money - stolen_amount
    player_to_win_money.money = player_to_win_money.money + stolen_amount
    player_to_win_money.save()
    player_to_lose_money.save()
    return stolen_amount

@login_required(login_url='/login')
def history(request):
    """History page"""
    fights_history = Fight.objects.filter(dragon_winner_owner=request.user) | Fight.objects.filter(dragon_loser_owner=request.user)
    context = {
        'fights': fights_history
    }
    return render(request, 'history.html', context)

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            player = Player()
            player.user = user
            player.money=1000
            player.save()
            return redirect("/login")
    else:
        form = RegisterUserForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)
