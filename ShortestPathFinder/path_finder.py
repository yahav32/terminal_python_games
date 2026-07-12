import curses
from curses import wrapper
import queue
import time
from typing import List, Tuple, Optional


maze = [
    ["#", "X", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "O", "#"]
]


class Maze:
    """Represents the maze structure, handles cell validation, coordinate lookup, and rendering."""
    
    def __init__(self, maze: List[List[str]] = []) -> None:
        """
        Initializes the maze representation and registers curses color pairs.
        
        param maze: 2D list representing the grid layout of the maze.
        """
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0]) if self.rows > 0 else 0

        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK) # red for exit/start
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK) # green for the algorithm
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK) # blue for the wall

    def draw(self, stdscr: curses.window, path: List[Tuple[int, int]] = []) -> None:
        """
        Draws the maze layout and the active path on the terminal screen.
        
        param stdscr: Curses screen window object.
        param path: List of (row, col) coordinates representing the path to draw.
        """
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if (i, j) in path:
                    stdscr.addstr(i * 2, j * 4, "X", curses.color_pair(2))
                elif value in ("O", "X"):
                    stdscr.addstr(i * 2, j * 4, value, curses.color_pair(1))
                else:
                    stdscr.addstr(i * 2, j * 4, value, curses.color_pair(3))

    def find_symbol(self, symbol: str) -> Optional[Tuple[int, int]]:
        """
        Searches for a specific symbol in the maze and returns its coordinates.
        
        param symbol: Character to search for (e.g., 'O', 'X').
        return: (row, col) if found, otherwise None.
        """
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if value == symbol:
                    return i, j
        return None

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Checks if the given cell is within the maze boundaries and is not a wall.
        
        param row: Row index.
        param col: Column index.
        return: True if the position is walkable, False otherwise.
        """
        return 0 <= row < self.rows and 0 <= col < self.cols and self.maze[row][col] != "#"

    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Retrieves all valid adjacent neighbors (up, down, left, right) for a given cell.
        
        param row: Row index.
        param col: Column index.
        return: List of valid neighbor coordinates.
        """
        neighbors = []
        for deltaRow, deltaCol in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row, new_col = row + deltaRow, col + deltaCol
            if self.is_valid_position(new_row, new_col):
                neighbors.append((new_row, new_col))
        return neighbors


class BFSPathFinder:
    """Handles pathfinding logic using the Breadth-First Search (BFS) algorithm."""
    
    def find_path(self, maze: Maze, stdscr: curses.window, start: str = "O", end: str = "X") -> List[Tuple[int, int]]:
        """
        Finds the shortest path from the start symbol to the end symbol using BFS.
        Clears and redraws the screen at each step to visualize the search progress.
        
        param maze: Maze instance containing the grid.
        param stdscr: Curses screen window object.
        param start: Starting symbol.
        param end: Ending symbol.
        return: List of coordinates representing the shortest path, or empty list if no path exists.
        """
        start_pose = maze.find_symbol(start)
        if not start_pose:
            return []

        q = queue.Queue()
        q.put((start_pose, [start_pose]))

        visited = {start_pose}

        while not q.empty():
            curr_pos, path = q.get()
            row, col = curr_pos

            stdscr.clear()
            maze.draw(stdscr, path)
            stdscr.refresh()
            time.sleep(0.3)

            if maze.maze[row][col] == end:
                return path

            for neighbor in maze.get_neighbors(row, col):
                if neighbor not in visited:
                    visited.add(neighbor)
                    q.put((neighbor, path + [neighbor]))

        return []


def main(stdscr: curses.window) -> None:
    """
    Main execution loop managing the curses window, initializing objects,
    and running the visualization.
    """
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    err, msg = curses.color_pair(4), curses.color_pair(5)

    height, width = stdscr.getmaxyx()
    if height < 18 or width < 18:
        stdscr.clear()
        stdscr.addstr(0, 0, "Error: Terminal is too small!", err)
        stdscr.addstr(1, 0, "Please resize your terminal to at least 18x18 and try again.", msg)
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    mazeObj = Maze(maze)
    path_finder = BFSPathFinder()
    path = path_finder.find_path(mazeObj, stdscr)
    mazeObj.draw(stdscr, path)
    stdscr.refresh()
    stdscr.getch()

wrapper(main)