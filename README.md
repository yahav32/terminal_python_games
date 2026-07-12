# Terminal Python Games

A collection of interactive terminal-based games developed in Python. This repository features a variety of games.

---

## Included Games (Ordered by Difficulty)

### 1. XO - Tic Tac Toe (`XO/`) — **Easy**
The classic game of Tic-Tac-Toe played directly in your terminal.
- **Features:**
  - Two-player local gameplay.
  - Input validation and win detection.
  - Clean terminal UI.
- **How to Run:**
  ```bash
  python XO/xo.py
  ```

### 2. Adventure Game (`AdvantureGame/`) — **Easy**
A text-based RPG where choices matter. Explore a mysterious world, manage your resources, and survive encounters.
- **Features:** 
  - Player health and strength stats.
  - Inventory system.
  - Monster encounters and combat.
  - Branching storylines based on user input.
- **How to Run:**
  ```bash
  python AdvantureGame/game_advanture.py
  ```

### 3. Quiz Game (`QuizGame/`) — **Medium**
A multi-user quiz application built using a **Client-Server architecture**.
- **Features:**
  - Centralized server managing questions and scores.
  - Multi-client support using Python Sockets.
  - Real-time interaction and scoring.
- **How to Run:**
  1. Start the server:
     ```bash
     python QuizGame/quiz_server.py
     ```
  2. Connect one or more clients:
     ```bash
     python QuizGame/quiz_client.py
     ```

### 4. Shortest Path Finder (`ShortestPathFinder/`) — **Hard**
A visual pathfinder in the terminal that supports both **Breadth-First Search (BFS)** and **A\* (A-Star)** algorithms to find the shortest path from start ('O') to end ('X') in a maze.
- **Features:**
  - Curses-based real-time terminal animation/visualization.
  - Visualization of explored cells during the search progress.
  - Implementations for both BFS and A* pathfinding.
  - Custom boundary checks and dynamic terminal size validation.
- **How to Run:**
  ```bash
  python ShortestPathFinder/path_finder.py
  ```
  *(Note: Requires a terminal with curses support)*

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
- **Curses**: For terminal-based GUI and visualization in the Shortest Path Finder.
