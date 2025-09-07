from fastapi import APIRouter, Form
from .. import battle_logic

router = APIRouter()

# Endpoint for the original terminal viewer
@router.post("/battle")
async def simulate_pokemon_battle(pokemon1: str, pokemon2: str):
    return await battle_logic.simulate_battle(pokemon1, pokemon2)

# Endpoint for the new Web UI LLM battle
@router.post("/battle-vs-llm")
async def simulate_battle_vs_llm(
    pokemon1: str = Form(), 
    pokemon2: str = Form()
):
    """Simulates a battle between a player (pokemon1) and an LLM (pokemon2)."""
    return await battle_logic.simulate_battle(
        pokemon1, pokemon2, llm_trainer_name=pokemon2
    )
