# Campus Route Finder – AI Lab Mini Project

**Title:** TCE Campus Route Finder using A* Search and Uniform Cost Search  
**Subject:** Artificial Intelligence Laboratory (Experiment 2: Uninformed & Informed Search Strategies)  
**Institution:** Thiagarajar College of Engineering (TCE), Madurai  
**Language:** Python 3 (Standard Library Only)

---

## 1. Abstract
Navigating a large university campus efficiently requires finding the shortest walking path between buildings connected by a network of walkways. This mini-project models the **Thiagarajar College of Engineering (TCE)** campus as a weighted undirected graph of 10 key landmarks and 16 two-way roads. It implements and compares two fundamental Artificial Intelligence search algorithms: **Uniform Cost Search (UCS)** (an uninformed search algorithm) and **A\* Search** (an informed, heuristic-guided search algorithm). Using the Euclidean straight-line distance as an admissible and consistent heuristic, the system demonstrates that while both algorithms are complete and optimal—always finding the exact same shortest path—**A\* Search expands significantly fewer nodes** by directing its search toward the goal.

---

## 2. Aim
To design and implement a Python program that finds the shortest walking route between two locations on the TCE campus using **Uniform Cost Search (UCS)** and **A\* Search**, and to compare their optimality and search efficiency (number of nodes expanded).

---

## 3. Objectives
1. To model real landmarks of the **TCE Campus** as nodes with 2D Cartesian coordinates `(x, y)` and walkways as weighted undirected edges.
2. To implement **Uniform Cost Search (UCS)** using a priority queue ordered by cumulative path cost $f(n) = g(n)$.
3. To formulate an **admissible heuristic** $h(n)$ using Euclidean straight-line distance and implement **A\* Search** ordered by $f(n) = g(n) + h(n)$.
4. To compare the performance of UCS and A\* Search across multiple campus routes in terms of total path distance and number of nodes expanded.

---

## 4. Algorithms & Heuristic Function

### 4.1 Uniform Cost Search (UCS)
Uniform Cost Search is an **uninformed (blind) search** strategy that expands the node with the lowest cumulative path cost from the start node. It uses no domain-specific knowledge about the goal's location.
- **Evaluation Function:**
  $$f(n) = g(n)$$
  where $g(n)$ is the actual road distance travelled from the start node to node $n$.
- **Properties:** Complete and Optimal (provided all edge costs are positive, $\text{cost} \ge \epsilon > 0$).

### 4.2 A* Search
A\* Search is an **informed (best-first) search** strategy that combines the actual cost to reach a node $g(n)$ with an estimated cost to reach the goal $h(n)$.
- **Evaluation Function:**
  $$f(n) = g(n) + h(n)$$
  where:
  - $g(n)$ = actual road distance from the start node to node $n$.
  - $h(n)$ = estimated straight-line distance from node $n$ to the goal node.
- **Properties:** Complete and Optimal when $h(n)$ is **admissible** (never overestimates the true cost to reach the goal).

### 4.3 Heuristic Function & Admissibility Proof
For any two campus buildings $A(x_1, y_1)$ and $B(x_2, y_2)$ (where $1 \text{ unit} = 100 \text{ metres}$):
- **Heuristic $h(n)$ (Euclidean Distance):**
  $$h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2} \times 100$$
- **Actual Road Cost:** Since campus footpaths curve around buildings and lawns, the actual walking road distance between connected locations is modelled as:
  $$\text{Road Cost}(A, B) = \text{round}\big(1.2 \times \text{Straight-Line Distance}(A, B)\big)$$
- **Why $h(n)$ is Admissible:** By geometry, a straight line is the shortest possible distance between two points in Euclidean space. Since every road edge is $20\%$ longer than the straight-line distance ($1.2 \times d$), the heuristic $h(n)$ never overestimates the true shortest walking path cost $h^*(n)$, satisfying $0 \le h(n) \le h^*(n)$. It also satisfies the triangle inequality, making it **consistent (monotonic)**.

---

## 5. Step-by-Step Algorithm

1. **Graph Initialization:**
   - Store the 10 TCE campus locations with their `(x, y)` coordinates in `LOCATIONS`.
   - For each road pair `(a, b)` in `ROADS`, compute the edge weight as `round(straight_line(a, b) * 1.2)` and add undirected edges `graph[a][b]` and `graph[b][a]`.
2. **Input Selection:**
   - Display the numbered list of 10 TCE campus buildings.
   - Read the user's `start` and `goal` location numbers.
3. **Priority Queue Search (`search(start, goal, use_heuristic)`):**
   - Initialize a min-heap priority queue `frontier` with tuple `(f, g, node, path) = (0, 0, start, [start])`.
   - Initialize dictionary `best_g = {start: 0}` to track the lowest known cost to each node, and set `nodes_expanded = 0`.
4. **Loop until `frontier` is empty:**
   - Pop the tuple `(f, g, node, path)` with the smallest `f` value from `frontier`.
   - If `g > best_g[node]`, skip this outdated queue entry.
   - Increment `nodes_expanded` by 1.
   - **Goal Test:** If `node == goal`, return `(path, g, nodes_expanded)`.
   - **Neighbour Expansion:** For each `neighbour` and edge `cost` of `node`:
     - Calculate `new_g = g + cost`.
     - If `new_g < best_g.get(neighbour, ∞)`:
       - Update `best_g[neighbour] = new_g`.
       - Compute `h = heuristic(neighbour, goal)` if running **A\***, or `h = 0` if running **UCS**.
       - Push `(new_g + h, new_g, neighbour, path + [neighbour])` into `frontier`.
5. **Output & Comparison:**
   - Display the shortest path, total distance in metres, and nodes expanded for both UCS and A\* Search, along with the node savings achieved by A\*.

---

## 6. Campus Map Topology

| # | TCE Building Name | Coordinates `(x, y)` | Connected Neighbours |
| :-: | :--- | :-: | :--- |
| 1 | **TCE Main Gate** | `(0, 0)` | Main Admin Block, Central Library, Mechanical Department |
| 2 | **Main Admin Block** | `(2, 1)` | TCE Main Gate, TCE Food Court, Central Library |
| 3 | **Central Library** | `(4, 0)` | TCE Main Gate, Main Admin Block, CSE Department |
| 4 | **TCE Food Court** | `(3, 3)` | Main Admin Block, CSE Department, KS Auditorium, Mechanical Department |
| 5 | **CSE Department** | `(6, 1)` | Central Library, TCE Food Court, ECE Department |
| 6 | **ECE Department** | `(6, 4)` | CSE Department, KS Auditorium, Men's Hostel |
| 7 | **Mechanical Department** | `(1, 4)` | TCE Main Gate, TCE Food Court, TCE Open Ground |
| 8 | **KS Auditorium** | `(4, 5)` | TCE Food Court, ECE Department, TCE Open Ground, Men's Hostel |
| 9 | **TCE Open Ground** | `(2, 7)` | Mechanical Department, KS Auditorium, Men's Hostel |
| 10 | **Men's Hostel** | `(7, 7)` | ECE Department, KS Auditorium, TCE Open Ground |

---

## 7. Full Source Code (`campus_route_finder.py`)

```python
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
```

---

## 8. Sample Output from a Real Run

```text
============================================================
   TCE CAMPUS ROUTE FINDER (A* Search vs Uniform Cost Search)
============================================================
   1. TCE Main Gate
   2. Main Admin Block
   3. Central Library
   4. TCE Food Court
   5. CSE Department
   6. ECE Department
   7. Mechanical Department
   8. KS Auditorium
   9. TCE Open Ground
  10. Men's Hostel

Enter START location number: 1
Enter GOAL location number : 10

[Uniform Cost Search]
  Path          : TCE Main Gate -> Main Admin Block -> TCE Food Court -> KS Auditorium -> Men's Hostel
  Total distance: 1237 metres
  Nodes expanded: 10

[A* Search]
  Path          : TCE Main Gate -> Main Admin Block -> TCE Food Court -> KS Auditorium -> Men's Hostel
  Total distance: 1237 metres
  Nodes expanded: 6

Comparison:
  Both found the same shortest distance: True
  A* expanded 4 fewer node(s) than UCS

Find another route? (y/n): y

Enter START location number: 7
Enter GOAL location number : 5

[Uniform Cost Search]
  Path          : Mechanical Department -> TCE Food Court -> CSE Department
  Total distance: 701 metres
  Nodes expanded: 7

[A* Search]
  Path          : Mechanical Department -> TCE Food Court -> CSE Department
  Total distance: 701 metres
  Nodes expanded: 3

Comparison:
  Both found the same shortest distance: True
  A* expanded 4 fewer node(s) than UCS

Find another route? (y/n): n
Thank you!
```

---

## 9. Result & Comparison Table

| Test Case | Start Location | Goal Location | Shortest Path Found (Both UCS & A*) | Distance (m) | UCS Nodes Expanded | A* Nodes Expanded | Fewer Nodes by A* |
| :-: | :--- | :--- | :--- | :-: | :-: | :-: | :-: |
| 1 | TCE Main Gate | Men's Hostel | TCE Main Gate $\rightarrow$ Main Admin Block $\rightarrow$ TCE Food Court $\rightarrow$ KS Auditorium $\rightarrow$ Men's Hostel | 1237 m | 10 | 6 | **4 (40% saved)** |
| 2 | TCE Main Gate | KS Auditorium | TCE Main Gate $\rightarrow$ Main Admin Block $\rightarrow$ TCE Food Court $\rightarrow$ KS Auditorium | 804 m | 7 | 4 | **3 (43% saved)** |
| 3 | Mechanical Dept | CSE Department | Mechanical Department $\rightarrow$ TCE Food Court $\rightarrow$ CSE Department | 701 m | 7 | 3 | **4 (57% saved)** |
| 4 | Main Admin Block | ECE Department | Main Admin Block $\rightarrow$ TCE Food Court $\rightarrow$ KS Auditorium $\rightarrow$ ECE Department | 804 m | 8 | 5 | **3 (38% saved)** |
| 5 | Central Library | TCE Open Ground | Central Library $\rightarrow$ Main Admin Block $\rightarrow$ TCE Food Court $\rightarrow$ KS Auditorium $\rightarrow$ TCE Open Ground | 1143 m | 10 | 8 | **2 (20% saved)** |

---

## 10. Conclusion
The **TCE Campus Route Finder** was successfully implemented in Python 3 using **Uniform Cost Search (UCS)** and **A\* Search**. Across all test cases on the 10-building TCE campus map:
1. **Optimality:** Both UCS and A\* Search consistently found the exact same shortest walking route and distance in metres.
2. **Efficiency:** Because A\* Search uses an admissible Euclidean straight-line heuristic $h(n)$, it focuses exploration toward the destination and expands up to **40%–57% fewer nodes** than Uniform Cost Search.

---

## 11. 10 Likely Viva Questions with Short Answers

**Q1. What is the main difference between Uniform Cost Search (UCS) and A\* Search?**  
**Ans:** UCS is an *uninformed* search algorithm that orders nodes purely by cumulative path cost $f(n) = g(n)$, expanding outward in all directions. A\* is an *informed* search algorithm that adds a heuristic estimate $f(n) = g(n) + h(n)$ to guide the search directly toward the goal.

**Q2. What heuristic function is used in this project, and why is it admissible?**  
**Ans:** We use the straight-line (Euclidean) distance between two campus locations as $h(n)$. It is admissible because a straight line is the shortest possible distance between two points, and our actual roads are $20\%$ longer ($\text{cost} = 1.2 \times \text{straight line}$), so $h(n)$ never overestimates the true walking distance.

**Q3. What happens if $h(n) = 0$ for all nodes in A\* Search?**  
**Ans:** When $h(n) = 0$, the evaluation function $f(n) = g(n) + 0$ reduces to $f(n) = g(n)$, which means A\* Search behaves identically to Uniform Cost Search (UCS). In fact, our code uses a single `search()` function with a `use_heuristic` boolean flag to demonstrate this exact relationship.

**Q4. What data structure is used to implement the frontier in UCS and A\*, and why?**  
**Ans:** A **min-heap priority queue** (`heapq` in Python) is used. It allows us to always extract the node with the minimum $f(n)$ value in $O(\log V)$ time.

**Q5. Why do we perform the goal test when *popping* a node from the priority queue rather than when *pushing* it?**  
**Ans:** Because the first time a goal node is *generated* (pushed), it might be reached via a suboptimal path with a higher cost. Only when the goal node is *popped* from the min-heap are we guaranteed that no other path in the frontier has a smaller cost $f(n)$.

**Q6. What does line `if g > best_g.get(node, math.inf): continue` do in the code?**  
**Ans:** Since Python's `heapq` does not support a native `decrease-key` operation, whenever we find a shorter path to a neighbour we push a new entry into the heap. This check lazily ignores older, higher-cost entries for the same node when they are eventually popped.

**Q7. Under what condition is Uniform Cost Search guaranteed to be optimal?**  
**Ans:** UCS is guaranteed to be optimal and complete as long as every edge cost is strictly positive ($\text{cost}(u, v) \ge \epsilon > 0$), preventing infinite zero-cost or negative-cost loops.

**Q8. What happens if the heuristic $h(n)$ overestimates the actual cost (i.e., is not admissible)?**  
**Ans:** If $h(n)$ overestimates the true cost to the goal, A\* Search loses its **optimality** guarantee—it may return a suboptimal path because the optimal path's $f(n)$ might look artificially high.

**Q9. What is a consistent (monotonic) heuristic, and is our Euclidean heuristic consistent?**  
**Ans:** A heuristic is consistent if $h(n) \le \text{cost}(n, n') + h(n')$ for every neighbour $n'$. Yes, our Euclidean straight-line distance satisfies the geometric triangle inequality, and since road costs are $1.2 \times$ straight-line distance, it is strictly consistent.

**Q10. Why did UCS expand all 10 nodes when searching from TCE Main Gate to Men's Hostel, whereas A\* expanded only 6?**  
**Ans:** `Men's Hostel` is at the far corner `(7, 7)` with a shortest path distance of $1237\text{ m}$, which is the furthest node from `TCE Main Gate (0, 0)`. UCS expands all nodes whose distance from the start is less than $1237\text{ m}$ (which happens to be the entire campus). A\* adds the remaining distance to `Men's Hostel`, pruning off-direction buildings like `Central Library` and `CSE Department` early.
