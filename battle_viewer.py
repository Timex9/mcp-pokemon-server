# battle_viewer.py
import requests
import sys
import time
import questionary
from rich.console import Console
import ascii_art

console = Console()

def get_pokemon_list():
    """Fetches the list of Pokémon from our server."""
    try:
        console.print("Fetching all Pokémon, this might take a moment on the first run...", style="yellow")
        response = requests.get("http://127.0.0.1:8000/resource/pokemon/list")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        console.print(f"Error: Could not fetch Pokémon list from the server. Is it running? Details: {e}", style="bold red")
        return None

def display_battle_art(p1, p2):
    """Displays the ASCII art for two Pokémon side-by-side."""
    art1 = ascii_art.get_art(p1).split('\n')
    art2 = ascii_art.get_art(p2).split('\n')

    # Pad the shorter art with blank lines to match the height of the taller one
    while len(art1) < len(art2):
        art1.append('')
    while len(art2) < len(art1):
        art2.append('')

    console.print("\n" * 2)
    for i in range(len(art1)):
        console.print(f"{art1[i]:<30}{'VS':^10}{art2[i]:<30}", justify="center", style="bold yellow")
    
    console.print("\n" * 2)
    time.sleep(2)

def watch_battle(p1, p2):
    """Prints the battle log with colors and styles."""
    console.print("\nConnecting to the battle server...", style="yellow")
    try:
        # Note: This endpoint is for a random battle, not the LLM one.
        response = requests.post(f"http://127.0.0.1:8000/tool/battle?pokemon1={p1}&pokemon2={p2}")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        console.print(f"Error: Could not connect to the server. Is it running? Details: {e}", style="bold red")
        return

    data = response.json()
    if data.get("error"):
        console.print(f"Server Error: {data['error']}", style="bold red")
        return
    
    console.print("\n--- Battle Starting! ---\n", style="bold magenta")
    time.sleep(1)
    
    # This logic assumes the 'log' is a simple list of strings from your basic battle endpoint
    if isinstance(data.get("log"), list):
        for line in data["log"]:
            if "super effective" in line:
                console.print(line, style="bold green")
            elif "not very effective" in line:
                console.print(line, style="dim yellow")
            elif "fainted" in line or "deals" in line:
                console.print(line, style="bold red")
            elif "afflicted" in line or "hurt by" in line:
                console.print(line, style="cyan")
            else:
                console.print(line)
            time.sleep(1.5)
        
        console.print("\n--- Battle Over! ---", style="bold magenta")
        console.print(f"🏆 The winner is {data['winner'].title()}! 🏆", style="bold yellow on blue")
    else:
        console.print("Received an unexpected battle log format from the server.", style="bold red")


def main():
    """Main function to run the interactive menu."""
    pokemon_names = get_pokemon_list()
    if not pokemon_names:
        return

    console.print("✅ Pokémon list loaded.", style="green")

    fighters = questionary.checkbox(
        "Select exactly two Pokémon to fight:",
        choices=pokemon_names,
        validate=lambda result: True if len(result) == 2 else "Please select exactly two Pokémon."
    ).ask()

    if fighters and len(fighters) == 2:
        p1, p2 = fighters[0], fighters[1]
        display_battle_art(p1, p2)
        watch_battle(p1, p2)
    else:
        console.print("No battle was run.", style="yellow")

if __name__ == "__main__":
    main()
