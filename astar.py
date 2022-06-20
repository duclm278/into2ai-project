import game
import prune
import heapq

class Fringe():
    # Node: (state, actions)
    def __init__(self):
        self.states = []
        self.active = {}
        self.counter = 0

    def add(self, node, priority):
        self.counter += 1
        node_state, node_actions = node
        entry = (priority, self.counter, node_state)
        heapq.heappush(self.states, entry)
        self.active[node_state] = (priority, node_actions)

    def contains_state(self, state):
        return state in self.active

    def delete(self, state):
        self.active.pop(state)

    def empty(self):
        return len(self.states) == 0
    
    def priority(self, state):
        return self.active[state][0]

    def remove(self):
        while self.states:
            state = heapq.heappop(self.states)[-1]
            if state in self.active:
                actions = self.active[state][-1]
                self.active.pop(state)
                return (state, actions)

class AStar():
    def __init__(self, level):
        self.board = level
        self.num_explored = 0
        self.num_deadlocked = 0
        self.max_stored = 0
        self.solution = None

    # def heuristic(self, boxes, goals):
    #     return len(set(boxes).difference(goals))

    def heuristic(self, boxes, goals):
        result = 0
        for box in set(boxes).difference(goals):
            min_distance = float("inf")
            for goal in set(goals).difference(boxes):
                distance = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                min_distance = min(min_distance, distance)

            result += min_distance

        return result

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
        start = ((boxes, robot), [None])
        fringe = Fringe()
        fringe.add(start, self.heuristic(boxes, goals))
        num_stored += 1
        max_stored += 1

        # Keep looping until solution found
        while True:
            # If nothing left in fringe, then no solution
            if fringe.empty():
                return

            # Choose a node from the fringe
            node = fringe.remove()
            node_state, node_actions = node
            num_stored -= 1

            # If node is the goal, then we have a solution
            if game.solved(node_state[0], goals):
                self.num_explored = len(explored)
                self.num_deadlocked = num_deadlocked
                self.max_stored = max_stored
                self.solution = "".join(node_actions[1:])
                return

            # Mark state as explored
            explored.add(node_state)
            num_stored += 1

            # Add neighbors to fringe
            next_g = len(node_actions) - 1 + 1
            for action in game.find_moves(node_state, walls):
                neighbor = game.next_state(node_state, action)
                if not fringe.contains_state(neighbor):
                    if neighbor not in explored:
                        if prune.locked(neighbor[0], goals, walls):
                            num_deadlocked += 1
                        else:
                            next_h = self.heuristic(neighbor[0], goals)
                            fringe.add((neighbor, node_actions + [action[0]]), next_g + next_h)
                            num_stored += 1
                else:
                    next_h = self.heuristic(neighbor[0], goals)
                    if next_g + next_h < fringe.priority(neighbor):
                        fringe.delete(neighbor)
                        fringe.add((neighbor, node_actions + [action[0]]), next_g + next_h)

            max_stored = max(max_stored, num_stored)