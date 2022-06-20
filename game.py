import bisect
import re

# Symbols
WALL = "#"
ROBOT = "@"
ROBOT_ON_STORAGE = "+"
BOX = "$"
BOX_ON_STORAGE = "*"
STORAGE = "."
FLOOR = " "

# Vectors
U = (-1,  0)
D = ( 1,  0)
L = ( 0, -1)
R = ( 0,  1)

def find_boxes(board):
    boxes = []
    for i, line in enumerate(board):
        for j, square in enumerate(line):
            if square in [BOX, BOX_ON_STORAGE]:
                boxes.append((i, j))
    
    return tuple(boxes)

def find_goals(board):
    goals = []
    for i, line in enumerate(board):
        for j, square in enumerate(line):
            if square in [STORAGE, BOX_ON_STORAGE, ROBOT_ON_STORAGE]:
                goals.append((i, j))
    
    return tuple(goals)

def find_moves(state, walls):
    candidates = [
        ("u", U),
        ("d", D),
        ("l", L),
        ("r", R),
    ]

    result = []
    boxes, robot = state
    for candidate in candidates:
        vector = candidate[1]
        r1, c1 = next_point(robot, vector)
        r2, c2 = next_point((r1, c1), vector)

        if (r1, c1) in boxes:
            final = (r2, c2)
            candidate = (candidate[0].upper(), vector)
        else:
            final = (r1, c1)

        if final not in boxes + walls:
            result.append(candidate)

    return tuple(result)

def find_robot(board):
    for i, line in enumerate(board):
        for j, square in enumerate(line):
            if square in [ROBOT, ROBOT_ON_STORAGE]:
                return (i, j)

def find_walls(board):
    walls = []
    for i, line in enumerate(board):
        for j, square in enumerate(line):
            if square == WALL:
                walls.append((i, j))
    
    return tuple(walls)

def group(solution, n):
    if not solution:
        return "No solution"

    return " ".join([solution[i:i+n] for i in range(0, len(solution), n)])

def output(board):
    for line in board:
        print(" ".join(line).rstrip())

def parse(filename):
    text = ""
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    # Clean text
    text = text.rstrip()
    text = re.sub(r";.*\n", "", text)

    levels = []
    blocks = text.split("\n\n")
    for block in blocks:
        levels.append(list2d(block))
    
    return levels

def list2d(block):
    contents = block.splitlines()
    num_rows = len(contents)
    num_cols = max(len(line) for line in contents)

    result = []
    for i in range(num_rows):
        line = []
        for j in range(num_cols):
            square = contents[i][j] if j < len(contents[i]) else " "
            line.append(square)

        result.append(line)

    return result

def next_point(point, vector):
    return (point[0] + vector[0], point[1] + vector[1])

def next_setup(setup, vector):
    from copy import deepcopy
    board, robot = deepcopy(setup)

    r0, c0 = robot
    r1, c1 = next_point((r0, c0), vector)
    r2, c2 = next_point((r1, c1), vector)

    square0 = board[r0][c0]
    square1 = board[r1][c1]
    square2 = ""
    if 0 <= r2 < len(board) and 0 <= c2 < len(board[0]):
        square2 = board[r2][c2]

    # Rules
    next_square0 = {
        ROBOT: FLOOR,
        ROBOT_ON_STORAGE: STORAGE,
    }
    next_square1 = {
        FLOOR: ROBOT,
        STORAGE: ROBOT_ON_STORAGE,
    }
    next_square1_push = {
        BOX: ROBOT,
        BOX_ON_STORAGE: ROBOT_ON_STORAGE,
    }
    next_square2 = {
        FLOOR: BOX,
        STORAGE: BOX_ON_STORAGE,
    }

    if square1 in next_square1:
        robot = (r1, c1)
        board[r0][c0] = next_square0[square0]
        board[r1][c1] = next_square1[square1]

    elif square1 in next_square1_push and square2 in next_square2:
        robot = (r1, c1)
        board[r0][c0] = next_square0[square0]
        board[r1][c1] = next_square1_push[square1]
        board[r2][c2] = next_square2[square2]

    return (board, robot)

def next_state(state, action):
    boxes, robot = state
    vector = action[1]

    r0, c0 = robot
    r1, c1 = next_point((r0, c0), vector)
    r2, c2 = next_point((r1, c1), vector)

    robot = (r1, c1)
    boxes = list(boxes)
    if action[0].isupper():
        boxes.remove((r1, c1))
        bisect.insort(boxes, (r2, c2))
    
    return (tuple(boxes), robot)

def solved(boxes, goals):
    return boxes == goals