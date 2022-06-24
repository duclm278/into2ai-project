import game
import prune

# Queue to store node
class Fringe():
    # node = (state, action) = ((box, robot), action)
    def __init__(self):
        self.fringe = []
        self.active = set()

    def add(self, node):
        node_state = node[0]
        self.fringe.append(node)
        self.active.add(node_state)

    def contains_state(self, state):
        return state in self.active

    def empty(self):
        # if len(self.fringe) == 0:
        #     return True
        return len(self.fringe) == 0

    def remove(self):
        if not self.empty():
            node_pop = self.fringe.pop(0)
            node_state, node_action = node_pop
            self.active.remove(node_state)
            return node_pop

class BFS():
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
        # node = (state , action) = ((box, robot), action)
        start = ((boxes, robot), [None])
        fringe = Fringe()
        fringe.add(start)
        
        # Keep looping until solution found
        while True:
            # If nothing left in fringe, then no solution.
            if fringe.empty():
                return
            else:
                # Choose a node from the fringe
                node = fringe.remove()
                num_stored -= 1
                # num_explored += 1
                node_state = node[0]
                node_boxes = node_state[0]
                node_actions = node[1]
                
                # Don't mark explored here, mark it later.
                # Here it isn't expanded to find neighbors.
                # If node is the goal, then we have a solution.
                # It will return immediately and won't enter for loop (find_moves).
                if game.solved(node_boxes, goals):
                    self.num_explored = len(explored)
                    self.num_deadlocked = num_deadlocked
                    self.max_stored = max_stored
                    self.solution = "".join(node_actions[1:])
                    return
                
                # Add neighbors to fringe
                for action in game.find_moves(node_state, walls):
                    # neighbor is a state
                    neighbor = game.next_state(node_state, action)
                    if not fringe.contains_state(neighbor):
                        if neighbor not in explored:
                            if prune.locked(neighbor[0], goals, walls):
                                num_deadlocked += 1
                            else:
                                fringe.add((neighbor, node_actions + [action[0]]))
                                num_stored += 1

                # Here the node has been expanded.
                # Mark explored here after entering for loop (find_moves)
                explored.add(node_state)
                num_stored += 1
                max_stored = max(max_stored, num_stored)
