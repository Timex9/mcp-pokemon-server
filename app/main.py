from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .endpoints import resource, tool  # We keep the API routers
from . import battle_logic, poke_api

app = FastAPI(
    title="Pokémon MCP Server",
    description="A server providing Pokémon data and battle simulations.",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

app.include_router(resource.router, prefix="/resource", tags=["Pokémon Data Resource"])
app.include_router(tool.router, prefix="/tool", tags=["Battle Simulation Tool"])


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    pokemon_list = await poke_api.get_all_pokemon_names()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "pokemon_list": pokemon_list}
    )

@app.post("/battle-pvp", response_class=HTMLResponse)
async def run_pvp_battle(request: Request, pokemon1: str = Form(), pokemon2: str = Form()):
    pokemon_list = await poke_api.get_all_pokemon_names()
    battle_result = await battle_logic.simulate_battle(pokemon1, pokemon2)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pokemon_list": pokemon_list,
            "battle_result": battle_result
        }
    )

@app.post("/battle-llm", response_class=HTMLResponse)
async def run_llm_battle(request: Request, pokemon1: str = Form(), pokemon2: str = Form()):
    pokemon_list = await poke_api.get_all_pokemon_names()
    battle_result = await battle_logic.simulate_battle(pokemon1, pokemon2, llm_trainer_name=pokemon2)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "pokemon_list": pokemon_list,
            "battle_result": battle_result
        }
    )
