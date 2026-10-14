"""
AI Lab Mini Project
Title  : TCE Campus Route Finder using A* Search and Uniform Cost Search
College: Thiagarajar College of Engineering (TCE), Madurai
Lang   : Python 3 (no external libraries needed)
"""

import heapq
import math

# ---------------------------------------------------------------
# 1. TCE Campus map: each location has (x, y) coordinates
#    1 unit = 100 metres
# ---------------------------------------------------------------
LOCATIONS = {
    "TCE Main Gate":          (0, 0),
    "Main Admin Block":       (2, 1),
    "Central Library":        (4, 0),
    "TCE Food Court":         (3, 3),
    "CSE Department":         (6, 1),
    "ECE Department":         (6, 4),
    "Mechanical Department":  (1, 4),
    "KS Auditorium":          (4, 5),
    "TCE Open Ground":        (2, 7),
    "Men's Hostel":           (7, 7),
}

# Two-way roads between TCE locations
ROADS = [
    ("TCE Main Gate", "Main Admin Block"),
    ("TCE Main Gate", "Central Library"),
    ("TCE Main Gate", "Mechanical Department"),
    ("Main Admin Block", "TCE Food Court"),
    ("Main Admin Block", "Central Library"),
    ("Central Library", "CSE Department"),
    ("TCE Food Court", "CSE Department"),
    ("TCE Food Court", "KS Auditorium"),
    ("TCE Food Court", "Mechanical Department"),
    ("CSE Department", "ECE Department"),
    ("ECE Department", "KS Auditorium"),
    ("ECE Department", "Men's Hostel"),
    ("Mechanical Department", "TCE Open Ground"),
    ("KS Auditorium", "TCE Open Ground"),
    ("KS Auditorium", "Men's Hostel"),
    ("TCE Open Ground", "Men's Hostel"),
]


def straight_line(a, b):
    """Straight-line (Euclidean) distance between two places in metres."""
    (x1, y1), (x2, y2) = LOCATIONS[a], LOCATIONS[b]
    return math.hypot(x1 - x2, y1 - y2) * 100


def build_graph():
    """Road length = straight-line distance + 20% (roads are not straight)."""
    graph = {place: {} for place in LOCATIONS}
    for a, b in ROADS:
        cost = round(straight_line(a, b) * 1.2)
        graph[a][b] = cost
        graph[b][a] = cost
    return graph


GRAPH = build_graph()


# ---------------------------------------------------------------
# 2. Heuristic for A*: straight-line distance to the goal.
#    It never overestimates the real road distance -> admissible.
# ---------------------------------------------------------------
def heuristic(node, goal):
    return straight_line(node, goal)


# ---------------------------------------------------------------
# 3. Common search function
#    UCS : f(n) = g(n)
#    A*  : f(n) = g(n) + h(n)
# ---------------------------------------------------------------
def search(start, goal, use_heuristic):
    frontier = [(0, 0, start, [start])]      # (f, g, node, path)
    best_g = {start: 0}
    nodes_expanded = 0

    while frontier:
        f, g, node, path = heapq.heappop(frontier)

        if g > best_g.get(node, math.inf):   # skip outdated entries
            continue

        nodes_expanded += 1

        if node == goal:                     # goal test
            return path, g, nodes_expanded

        for neighbour, cost in GRAPH[node].items():
            new_g = g + cost
            if new_g < best_g.get(neighbour, math.inf):
                best_g[neighbour] = new_g
                h = heuristic(neighbour, goal) if use_heuristic else 0
                heapq.heappush(frontier,
                               (new_g + h, new_g, neighbour, path + [neighbour]))

    return None, math.inf, nodes_expanded


def uniform_cost_search(start, goal):
    return search(start, goal, use_heuristic=False)


def a_star_search(start, goal):
    return search(start, goal, use_heuristic=True)


# ---------------------------------------------------------------
# 4. User interface
# ---------------------------------------------------------------
def choose_place(places, prompt):
    while True:
        choice = input(prompt).strip()
        if choice.isdigit() and 1 <= int(choice) <= len(places):
            return places[int(choice) - 1]
        print("  Invalid choice, enter a number from the list.")


def show_result(name, path, cost, expanded):
    print(f"\n[{name}]")
    if path is None:
        print("  No route found.")
        return
    print("  Path          :", " -> ".join(path))
    print("  Total distance:", cost, "metres")
    print("  Nodes expanded:", expanded)


def main():
    places = list(LOCATIONS)
    print("=" * 60)
    print("   TCE CAMPUS ROUTE FINDER (A* Search vs Uniform Cost Search)")
    print("=" * 60)
    for i, p in enumerate(places, 1):
        print(f"  {i:2}. {p}")

    while True:
        start = choose_place(places, "\nEnter START location number: ")
        goal = choose_place(places, "Enter GOAL location number : ")

        ucs = uniform_cost_search(start, goal)
        astar = a_star_search(start, goal)

        show_result("Uniform Cost Search", *ucs)
        show_result("A* Search", *astar)

        print("\nComparison:")
        print(f"  Both found the same shortest distance: {ucs[1] == astar[1]}")
        print(f"  A* expanded {ucs[2] - astar[2]} fewer node(s) than UCS")

        again = input("\nFind another route? (y/n): ").strip().lower()
        if again != "y":
            print("Thank you!")
            break


if __name__ == "__main__":
    main()
