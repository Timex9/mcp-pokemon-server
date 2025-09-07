# ascii_art.py

# A dictionary mapping lowercase Pokémon names to their ASCII art.
# Using triple quotes for multi-line strings.
POKEMON_ART = {
    "charizard": r"""
        / \
       | |
   _   | |   _
  / \  | |  / \
 |   \ | | /   |
 | |\ \| |/ /| |
 | | \ Y Y / | |
  \ \  _  / /
   \~`( )`~/
    `~` `~`
    """,
    "blastoise": r"""
       / \
      | |
      | |
  _  /| |\  _
 / \/ | | \/ \
|    `---`    |
| /' \ / `\ |
|/   /o\   \|
     \_/
    """,
    "venusaur": r"""
      /   \
     / / \ \
    | |   | |
    \ \ _ / /
     `-----`
  / /-----\ \
 / /       \ \
| |         | |
  \ \_____/ /
    `-----`
    """,
    "pikachu": r"""
      / \
     | |
     | | /`\
     | |<o o>
     | | \_/
     /   /
    /  /`
   /  /
    `~`
    """,
    "unknown": r"""
      .--.
     /..  \
    | ` \ |
    '-----'
      ( )
     '---'
    """
}

def get_art(pokemon_name):
    """Returns the ASCII art for a Pokémon, or a default if not found."""
    return POKEMON_ART.get(pokemon_name.lower(), POKEMON_ART["unknown"])
