import game
import prune

class Fringe():
    # Node: (state, actions)
    def __init__(self):
        raise NotImplementedError

    def add(self, node):
        raise NotImplementedError

    def contains_state(self, state):
        raise NotImplementedError

    def empty(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

class DFS():
    def __init__(self, level):
        self.board = level
        self.num_explored = 0
        self.num_deadlocked = 0
        self.max_stored = 0
        self.solution = None

    def solve(self):
        # Results
        explored = set()
        num_deadlocked = 0
        num_stored = 0
        max_stored = 0

        # Objects
        board = self.board
        boxes = game.find_boxes(board)
        goals = game.find_goals(board)
        robot = game.find_robot(board)
        walls = game.find_walls(board)

        # Initialize fringe to just the starting node
        raise NotImplementedError