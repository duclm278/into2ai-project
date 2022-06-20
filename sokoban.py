import argparse
import csv
import game
import time
from astar import AStar
from dfs import DFS
from bfs import BFS

def main():
    infile, method = get_commands()

    # Parse file
    levels = game.parse(infile)
    print(f"Loaded {len(levels)} level(s).")

    # Assess AI
    report = []
    for i, level in enumerate(levels):
        if method == "dfs":
            ai = DFS(level)
        elif method == "bfs":
            ai = BFS(level)
        elif method == "astar":
            ai = AStar(level)
        
        print(f"Level {i + 1}:")
        game.output(level)
        print("Solving...")

        start = time.perf_counter()
        ai.solve()
        total = time.perf_counter() - start
        total = "{:.4f}".format(total)

        # Group letters
        solution = game.group(ai.solution, 4)

        # Print results
        print(f"Explored: {ai.num_explored}")
        print(f"Locked: {ai.num_deadlocked}")
        print(f"Stored: {ai.max_stored}")
        print(f"Solution: {solution}")
        print(f"Time: {total}\n")

        report.append((i + 1, ai.num_explored, ai.num_deadlocked, ai.max_stored, len(ai.solution), total))

    # Save results in CSV format
    with open(f"{method}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(report)

    print(f"Saved results to {method}.csv.")

def get_commands():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("infile", help="read data from INFILE", metavar="INFILE")
    parser.add_argument("-m", "--method", choices=["astar", "bfs", "dfs"], help="select a search method", default="bfs")
    args = parser.parse_args()

    return args.infile, args.method

if __name__ == "__main__":
    main()