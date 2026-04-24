# Terminal Python Games

A collection of interactive terminal-based games developed in Python. This repository features a variety of games.

---

## Included Games

### 1. Adventure Game (`AdvantureGame/`)
A text-based RPG where choices matter. Explore a mysterious world, manage your resources, and survive encounters.
- **Features:** 
  - Player health and strength stats.
  - Inventory system.
  - Monster encounters and combat.
  - Branching storylines based on user input.

### 2. Quiz Game (`QuizGame/`)
A multi-user quiz application built using a **Client-Server architecture**.
- **Features:**
  - Centralized server managing questions and scores.
  - Multi-client support using Python Sockets.
  - Real-time interaction and scoring.
- **How to Run:**
  1. Start the server: `python QuizGame/quiz_server.py`
  2. Connect one or more clients: `python QuizGame/quiz_client.py`

### 3. XO - Tic Tac Toe (`XO/`)
The classic game of Tic-Tac-Toe played directly in your terminal.
- **Features:**
  - Two-player local gameplay.
  - Input validation and win detection.
  - Clean terminal UI.

---

## Getting Started

### Prerequisites
- **Python 3.x** installed on your system.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yahav32/terminal_python_games.git
   ```
2. Navigate to the project directory:
   ```bash
   cd terminal_python_games
   ```

---

## Technologies Used
- **Python**: Core logic.
- **Sockets**: Network communication for the Quiz Game.
- **Random**: For procedural events in the Adventure Game.
