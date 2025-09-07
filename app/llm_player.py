# app/llm_player.py
import google.generativeai as genai
import os

# --- IMPORTANT: PASTE YOUR API KEY HERE ---
# For better security, it's good practice to set this as an environment variable,
# but for this project, pasting it here is fine.
API_KEY = 'AIzaSyCuqTmnTPhNQAjp1rtisld8xWSQgBXiYn0'
# -----------------------------------------

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def construct_prompt(battle_state):
    """Creates a detailed prompt for the LLM to make a decision."""
    
    my_pokemon = battle_state['my_pokemon']
    opponent_pokemon = battle_state['opponent_pokemon']
    my_moves = battle_state['my_moves']

    # Create a simple, numbered list of moves for the LLM
    move_list_str = "\n".join([f"- {move}" for move in my_moves])

    prompt = f"""
    You are a strategic Pokémon trainer in a critical battle. It is your turn to choose a move.
    Analyze the situation carefully and choose the best move to use against your opponent to win.

    **Current Situation:**
    - Your Pokémon: {my_pokemon['name']} (Current HP: {my_pokemon['hp']})
    - Opponent's Pokémon: {opponent_pokemon['name']} (Current HP: {opponent_pokemon['hp']})

    **Your Available Moves:**
    {move_list_str}

    **Your Task:**
    Which of your available moves is the best strategic choice right now?
    Respond with ONLY the name of the move you want to use, exactly as it appears in the list.
    For example, if the best move is 'thunder-punch', your entire response should be just 'thunder-punch'.
    """
    return prompt

async def choose_move(battle_state):
    """Asks the Gemini model to choose a move."""
    prompt = construct_prompt(battle_state)
    try:
        response = await model.generate_content_async(prompt)
        # Clean up the response to get just the move name
        chosen_move = response.text.strip().lower()

        # Final check to ensure the chosen move is valid
        if chosen_move in battle_state['my_moves']:
            return chosen_move
        else:
            # If the LLM hallucinates a move, fall back to a random choice
            return "random"

    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # As a fallback, just pick a random move
        return "random"
