# app/endpoints/resource.py
from fastapi import APIRouter, HTTPException
from .. import poke_api, models

router = APIRouter()

# --- CORRECT ORDER ---
# The specific path '/list' now comes BEFORE the dynamic path '/{pokemon_name}'

@router.get("/pokemon/list")
async def get_pokemon_list():
    """Provides a list of all Pokémon names for the interactive menu."""
    names = await poke_api.get_all_pokemon_names()
    if not names:
        raise HTTPException(status_code=500, detail="Could not fetch Pokémon list.")
    return names

@router.get("/pokemon/{pokemon_name}", response_model=models.Pokemon)
async def get_pokemon_resource(pokemon_name: str):
    """
    Exposes comprehensive Pokémon data for a given Pokémon name or ID.
    This endpoint follows MCP resource design patterns by providing structured data.
    """
    data = await poke_api.get_pokemon_data(pokemon_name)
    
    if not data:
        raise HTTPException(status_code=404, detail="Pokémon not found")

    processed_data = {
        "id": data["id"],
        "name": data["name"],
        "types": [t["type"]["name"] for t in data["types"]],
        "abilities": [a["ability"]["name"] for a in data["abilities"]],
        "base_stats": [
            {"name": s["stat"]["name"], "value": s["base_stat"]}
            for s in data["stats"]
        ]
    }
    
    return processed_data
