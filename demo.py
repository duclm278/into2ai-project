import game
import sys

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python demo.py INFILE")

    levels = game.parse(sys.argv[1])
    print(f"Loaded {len(levels)} level(s).")
    for i, level in enumerate(levels):
        print(f"Level {i + 1}:")
        goals = game.find_goals(level)
        robot = game.find_robot(level)
        sequence = input("Sequence: ").replace(" ", "")
        if finished((level, robot), goals, sequence):
            print(f"Level {i + 1} solved!")
        else:
            sys.exit("Not solved yet!")

def finished(setup, goals, sequence):
    for action in sequence:
        game.output(setup[0])
        print()
        boxes = game.find_boxes(setup[0])

        if action.upper() == "U":
            setup = game.next_setup(setup, game.U)
            continue
        if action.upper() == "D":
            setup = game.next_setup(setup, game.D)
            continue
        if action.upper() == "L":
            setup = game.next_setup(setup, game.L)
            continue
        if action.upper() == "R":
            setup = game.next_setup(setup, game.R)
            continue

    game.output(setup[0])
    print()
    boxes = game.find_boxes(setup[0])
    return game.solved(boxes, goals)

if __name__ == "__main__":
    main()