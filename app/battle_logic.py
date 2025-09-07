#battle_logic.py
from . import llm_player
from . import poke_api
import math
import random

# A dictionary representing the type chart for damage multipliers
TYPE_CHART = {
    "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
    "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
    "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
    "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5},
    "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5},
    "poison": {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2},
    "ground": {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
    "flying": {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
    "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "dark": 2, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
    "ghost": {"normal": 0, "psychic": 2, "ghost": 2, "dark": 0.5},
    "dragon": {"dragon": 2, "steel": 0.5, "fairy": 0},
    "dark": {"fighting": 0.5, "psychic": 2, "ghost": 2, "dark": 0.5, "fairy": 0.5},
    "steel": {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2},
    "fairy": {"fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5}
}

def get_type_effectiveness(attack_type, defender_types):
    """Calculates the type effectiveness multiplier."""
    multiplier = 1.0
    for def_type in defender_types:
        effectiveness = TYPE_CHART.get(attack_type, {}).get(def_type)
        if effectiveness is not None:
            multiplier *= effectiveness
    return multiplier

def get_stat(stats_list, stat_name):
    """A helper function to find a stat's value from the raw 'stats' list."""
    for stat in stats_list:
        if stat['stat']['name'] == stat_name:
            return stat['base_stat']
    return 0

def calculate_damage(attacker_data, defender_data, move_data):
    """Calculates damage, accounting for physical vs. special moves."""
    if move_data is None or move_data.get("power") is None:
        return 0, 1.0

    level = 50
    move_power = move_data["power"]
    move_type = move_data["type"]["name"]
    damage_class = move_data["damage_class"]["name"]

    if damage_class == "physical":
        attack_stat = get_stat(attacker_data['stats'], 'attack')
        defense_stat = get_stat(defender_data['stats'], 'defense')
    elif damage_class == "special":
        attack_stat = get_stat(attacker_data['stats'], 'special-attack')
        defense_stat = get_stat(defender_data['stats'], 'special-defense')
    else:
        return 0, 1.0

    defender_types = [t['type']['name'] for t in defender_data['types']]
    type_multiplier = get_type_effectiveness(move_type, defender_types)
    
    damage = math.floor((((2 * level / 5 + 2) * move_power * attack_stat / defense_stat) / 50) + 2)
    final_damage = math.floor(damage * type_multiplier)

    return final_damage, type_multiplier

def determine_turn_order(p1_data, p2_data):
    """Determines which Pokémon attacks first based on their speed stat."""
    p1_speed = get_stat(p1_data['stats'], 'speed')
    p2_speed = get_stat(p2_data['stats'], 'speed')
    
    if p1_speed > p2_speed:
        return (p1_data, p2_data)
    else:
        return (p2_data, p1_data)

def apply_status_effect(attacker_data):
    """Randomly applies a status effect."""
    if random.random() < 0.1:
        return random.choice(["poison", "burn", "paralysis"])
    return None

async def simulate_battle(pokemon1_name: str, pokemon2_name: str, llm_trainer_name: str = None):
    p1_data = await poke_api.get_pokemon_data(pokemon1_name)
    p2_data = await poke_api.get_pokemon_data(pokemon2_name)
    
    if not p1_data or not p2_data:
        return {"error": "One or both Pokémon not found."}

    p1_hp = get_stat(p1_data['stats'], 'hp')
    p2_hp = get_stat(p2_data['stats'], 'hp')
    p1_max_hp = p1_hp
    p2_max_hp = p2_hp
    statuses = {p1_data['name']: None, p2_data['name']: None}
    
    battle_turns = []
    
    attacker, defender = determine_turn_order(p1_data, p2_data)
    
    while p1_hp > 0 and p2_hp > 0:
        turn_log = []
        
        if statuses[attacker['name']] == "paralysis" and random.random() < 0.25:
            turn_log.append(f"⚡️ {attacker['name'].title()} is fully paralyzed and can't move!")
            battle_turns.append({"text": " ".join(turn_log), "p1_hp_percent": (p1_hp / p1_max_hp) * 100, "p2_hp_percent": (p2_hp / p2_max_hp) * 100})
            attacker, defender = defender, attacker
            continue

        chosen_move_info = None
        if attacker['name'] == llm_trainer_name:
            pass 
        
        if chosen_move_info is None:
            damage_moves = [m['move'] for m in attacker['moves']]
            if not damage_moves:
                turn_log.append(f"❓ {attacker['name'].title()} has no moves!")
                battle_turns.append({"text": " ".join(turn_log), "p1_hp_percent": (p1_hp / p1_max_hp) * 100, "p2_hp_percent": (p2_hp / p2_max_hp) * 100})
                attacker, defender = defender, attacker
                continue
            chosen_move_info = random.choice(damage_moves)

        move_data = await poke_api.get_move_data(chosen_move_info['url'])

        if move_data is None or move_data.get("power") is None:
            turn_log.append(f"💨 {attacker['name'].title()} used {chosen_move_info['name']} but it had no effect!")
        else:
            turn_log.append(f"💥 {attacker['name'].title()} unleashes {move_data['name'].title()}!")
            damage, multiplier = calculate_damage(attacker, defender, move_data)
            if multiplier > 1: turn_log.append("It's super effective!")
            elif 0 < multiplier < 1: turn_log.append("It's not very effective...")
            
            turn_log.append(f"It deals {damage} damage!")
            if defender['name'] == p1_data['name']: p1_hp -= damage
            else: p2_hp -= damage
            p1_hp = max(0, p1_hp)
            p2_hp = max(0, p2_hp)

        battle_turns.append({"text": " ".join(turn_log), "p1_hp_percent": (p1_hp / p1_max_hp) * 100, "p2_hp_percent": (p2_hp / p2_max_hp) * 100})
        if p1_hp <= 0 or p2_hp <= 0: break
        attacker, defender = defender, attacker

    winner_name = p1_data['name'] if p1_hp > 0 else p2_data['name']
    

    p1_stats = [{"name": s['stat']['name'], "value": s['base_stat']} for s in p1_data['stats']]
    p2_stats = [{"name": s['stat']['name'], "value": s['base_stat']} for s in p2_data['stats']]

    return {
        "p1_initial": {"name": p1_data['name'].title(), "sprite": p1_data['sprites']['front_default'], "stats": p1_stats},
        "p2_initial": {"name": p2_data['name'].title(), "sprite": p2_data['sprites']['front_default'], "stats": p2_stats},
        "turns": battle_turns,
        "winner": winner_name
    }
       
