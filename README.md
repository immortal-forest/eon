# Echoes of the Nebula (EON)

A classic text-based adventure game built in Python, focusing on mystery, exploration, and survival in a sci-fi setting. This project was developed as part of the CITX1401 unit.

## About the Project

"Echoes of the Nebula" is an interactive terminal-based game where the player awakens as a lone technician on a derelict research vessel trapped in a mysterious cosmic nebula. The player must restore ship systems, confront strange entities, and make choices that determine their fate.

The game is built entirely in Python 3 using only the standard library, with a focus on creating a modular and clean codebase.

## Features

- **Branching Narrative:** A complete story with multiple paths and endings driven by player choice.
- **Dynamic Terminal UI:** A screen-painted interface that adapts to terminal size, using ANSI escape codes for color and positioning.
- **Turn-Based Combat:** A strategic combat system with attack/defend options and randomized elements.
- **Item Collection & Prerequisites:** An inventory system where items are required to unlock new choices and areas.
- **Save/Load System:** Players can save and load their progress at any time.
- **Advanced Visuals:** Includes ASCII art for combat, a typing animation for dialogue, and styled text to enhance immersion.
- **Random Encounters:** Certain areas have a chance to trigger a surprise combat encounter, adding replayability.

## How to Run

1. Clone the repository:
   ```sh
   git clone https://github.com/immortal-forest/eon.git
   ```
1. Navigate to the project directory:
   ```sh
   cd eon
   ```
1. Run the game:
   ```sh
   python main.py
   ```

## Tech Stack

- **Python 3.12** (No external packages required)
