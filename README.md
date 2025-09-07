# Pokémon Battle Simulation - MCP Server

This project is an advanced implementation of a Model Context Protocol (MCP) server, originally developed for a technical assessment. It provides a comprehensive Pokémon data resource and a dynamic battle simulation tool, accessible via a full-stack web application, an interactive terminal viewer, and a raw API.

## ✨ Features

This project goes far beyond a simple simulation and includes a wide range of advanced features:

* **Full-Stack Web Interface**: A user-friendly web UI built with FastAPI and Jinja2 for selecting Pokémon and watching battles.
* **Live Battle Commentary**: The web interface displays a running, auto-scrolling log of the battle, complete with animated health bars and Pokémon images.
* **Advanced Battle Engine**: The simulation logic features:
    * **Real Moves**: Pokémon select from their actual move sets fetched from the PokéAPI.
    * **Physical vs. Special Attacks**: The damage calculator correctly uses `Attack`/`Defense` for physical moves and `Special-Attack`/`Special-Defense` for special moves.
    * **Type Effectiveness** and **Status Effects** (Paralysis, Burn, Poison).
* **Player vs. LLM Mode**: A special battle mode where one of the Pokémon is controlled by the **Google Gemini LLM**, which makes strategic move choices.
* **Interactive Terminal Viewer**: For users who prefer the command line, an interactive viewer built with `rich` and `questionary` provides a colorful, menu-driven battle experience.
* **Core MCP API**: The underlying API provides a resource to get detailed data on any Pokémon.

## 💻 Tech Stack

* **Backend**: Python, FastAPI, Uvicorn
* **Frontend**: HTML, Jinja2, CSS, JavaScript
* **AI**: Google Gemini API
* **CLI**: Rich, Questionary
* **API Communication**: HTTPX

## 🚀 Setup and Installation

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone https://github.com/Timex9/mcp-pokemon-server.git
cd mcp_pokemon_server
```

### 2. Create and Activate Virtual Environment
```bash
# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Your Gemini API Key (Required for LLM Mode)
This project uses the Google Gemini API to power the "Player vs. LLM" mode.

1.  Get a free API key from **Google AI Studio**.
2.  Open the file `app/llm_player.py`.
3.  Paste your key into the `API_KEY` variable at the top of the file:
    ```python
    API_KEY = 'YOUR_API_KEY_HERE'
    ```
4.  Save the file.

## 🕹️ How to Use

### 1. Run the Server
With your virtual environment active, start the FastAPI server from the root project directory:
```bash
uvicorn app.main:app --reload
```
The server will be running at `http://127.0.0.1:8000`.

### 2. Use the Web Interface (Recommended)
This is the primary way to interact with the application.
* Open your web browser and navigate to **http://127.0.0.1:8000**.
* Select two Pokémon from the dropdowns.
* Choose your battle mode: "Player vs. Player" (a fast, automated simulation) or "Player vs. LLM" (a slower, strategic battle against the AI).

### 3. Use the Interactive Terminal Viewer
For a command-line experience:
* Make sure the server is running.
* Open a **new** terminal window, navigate to the project folder, and activate the virtual environment.
* Run the viewer script:
    ```bash
    python battle_viewer.py
    ```
* Follow the on-screen menu to select your fighters.