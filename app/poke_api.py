#poke_api.py
import httpx
import json

POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

pokemon_list_cache = []

async def get_all_pokemon_names():
    """Fetches a list of all Pokémon names from the PokéAPI."""
    global pokemon_list_cache
    if pokemon_list_cache:
        return pokemon_list_cache

    url = f"{POKEAPI_BASE_URL}pokemon?limit=1302"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            # Store names in the cache
            pokemon_list_cache = sorted([p['name'] for p in data['results']])
            return pokemon_list_cache
        except httpx.HTTPStatusError:
            return []


async def get_pokemon_data(pokemon_name: str):
    """Fetches data for a single Pokémon from the PokéAPI."""
    pokemon_name = pokemon_name.lower()
    url = f"{POKEAPI_BASE_URL}pokemon/{pokemon_name}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            return None


async def get_move_data(move_url: str):
    """Fetches data for a specific move from its URL."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(move_url)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            return None
