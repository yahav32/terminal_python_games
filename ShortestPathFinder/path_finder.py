import heapq
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
maze2 = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "O", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", " ", "#", " ", "#", "#", "#", "#", "#", " ", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", " ", "#", " ", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", "#", "#", "#", " ", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "X", "#", "#", "#", "#", "#"]
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
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # yellow for the explored
        
    def draw(self, stdscr: curses.window, path: List[Tuple[int, int]] = [], visited: List[Tuple[int, int]] = []) -> None:
        """
        Draws the maze layout, the active path, and the visited cells on the terminal screen.
        
        param stdscr: Curses screen window object.
        param path: List of (row, col) coordinates representing the path to draw.
        param visited: List of (row, col) coordinates representing the visited cells.
        """
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                position = (i, j)
                try:
                    if position in path:
                        stdscr.addstr(i * 2, j * 4, "X", curses.color_pair(2))
                    elif position in visited:
                        stdscr.addstr(i * 2, j * 4, ".", curses.color_pair(4))
                    elif value in ("O", "X"):
                        stdscr.addstr(i * 2, j * 4, value, curses.color_pair(1))
                    else:
                        stdscr.addstr(i * 2, j * 4, value, curses.color_pair(3))
                except curses.error:
                    pass

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



class AStar:
    def __init__(self, maze: Maze, start: str = "O", end: str = "X"):
        self.maze = maze
        self.start_pose = maze.find_symbol(start)
        self.goal = maze.find_symbol(end)
        self.open_set = []
        self.g_scores = {self.start_pose: 0}
        start_f = self.heuristic(self.start_pose, self.goal)
        heapq.heappush(self.open_set, (start_f, self.start_pose))
        self.came_from = {}
        self.visited = set()
    
    def heuristic(self, pose1: Tuple[int, int], pose2: Tuple[int, int]) -> int:
        """
        Calculates the heuristic (estimated cost) between two points.
        """
        return abs(pose1[0] - pose2[0]) + abs(pose1[1] - pose2[1])
    
    def reconstruct_path(self, end_pose: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstructs the path from the came_from dictionary to the given end position.
        """
        path = []
        current = end_pose
        while current != self.start_pose:
            path.append(current)
            if current not in self.came_from:
                return []
            current = self.came_from[current]
        path.append(self.start_pose)
        path.reverse()

        return path

    def find_path(self, maze: Maze, stdscr: curses.window) -> List[Tuple[int, int]]:
        """
        Finds the shortest path from the start symbol to the end symbol using A*.
        Clears and redraws the screen at each step to visualize the search progress.
        
        param maze: Maze instance containing the grid.
        param stdscr: Curses screen window object for visualization.
        return: List of coordinates representing the shortest path, or empty list if no path exists.
        """
        while self.open_set:
            f, current = heapq.heappop(self.open_set)

            if current in self.visited:
                continue

            self.visited.add(current)

            current_path = self.reconstruct_path(current)
            stdscr.clear()
            self.maze.draw(stdscr, current_path, list(self.visited))
            stdscr.refresh()
            time.sleep(0.3)

            if current == self.goal:
                final_path = self.reconstruct_path(self.goal)
                for i in range(1, len(final_path) + 1):
                    stdscr.clear()
                    self.maze.draw(stdscr, final_path[:i], list(self.visited))
                    stdscr.refresh()
                    time.sleep(0.3)
                return final_path

            row, col = current
            neighbors = self.maze.get_neighbors(row, col)
            for neighbor in neighbors:
                if neighbor in self.visited:
                    continue

                tentative_g = self.g_scores[current] + 1
                if tentative_g < self.g_scores.get(neighbor, float("inf")):
                    self.came_from[neighbor] = current
                    self.g_scores[neighbor] = tentative_g
                    f_score = tentative_g + self.heuristic(neighbor, self.goal)
                    heapq.heappush(self.open_set, (f_score, neighbor))
        return []

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

    mazeObj = Maze(maze2)
    req_height = mazeObj.rows * 2
    req_width = mazeObj.cols * 4

    height, width = stdscr.getmaxyx()
    if height < req_height or width < req_width:
        stdscr.clear()
        try:
            stdscr.addstr(0, 0, "Error: Terminal is too small!", err)
            stdscr.addstr(1, 0, f"Please resize your terminal to at least {req_height}x{req_width} (current: {height}x{width}) and try again.", msg)
        except curses.error:
            pass
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    # path_finder = BFSPathFinder()
    astar = AStar(mazeObj)
    path = astar.find_path(mazeObj, stdscr)
    mazeObj.draw(stdscr, path)
    stdscr.refresh()
    stdscr.getch()

wrapper(main)