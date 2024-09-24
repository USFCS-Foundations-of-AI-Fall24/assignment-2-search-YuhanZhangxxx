from queue import PriorityQueue
import math
from Graph import Graph, Node, Edge

def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True):
    frontier = PriorityQueue()  # Priority queue for the frontier
    closed_set = set()  # Closed set to keep track of visited states
    frontier.put(start_state)
    if use_closed_list:
        closed_set.add(start_state)
    state_counter = 0  # Counter for the number of states expanded
    while not frontier.empty():
        current_state = frontier.get()
        if goal_test(current_state):
            # Goal found, reconstruct the path
            path = []
            state = current_state
            while state:
                path.append(state)
                state = state.prev_state
            path.reverse()
            print(f"Total states: {state_counter}")
            return path
        edges = current_state.mars_graph.get_edges(Node(current_state.location)) or []
        successors = []
        for edge in edges:
            new_loc = edge.dest.value  # Get the location of the successor
            cost = current_state.g + edge.val  # Calculate new g value
            heuristic = heuristic_fn(map_state(new_loc, current_state.mars_graph))
            new_state = map_state(new_loc, current_state.mars_graph, current_state, cost, heuristic)
            if use_closed_list and new_state in closed_set:
                continue  # Skip if already in closed set
            successors.append(new_state)
            if use_closed_list:
                closed_set.add(new_state)
        state_counter += len(successors)  # Increment state counter
        for state in successors:
            frontier.put(state)
    print(f"Total states: {state_counter}")
    return None  # No path found

class map_state:
    def __init__(self, location="", mars_graph=None, prev_state=None, g=0, h=0):
        self.location = location  # Current location as a string (e.g., "1,1")
        self.mars_graph = mars_graph  # Reference to the Mars map graph
        self.prev_state = prev_state  # Reference to the previous state
        self.g = g  # Cost from start to current state
        self.h = h  # Heuristic estimate from current state to goal
        self.f = self.g + self.h  # Estimated total cost (f = g + h)

    def __eq__(self, other):
        # Equality based on location
        return isinstance(other, map_state) and self.location == other.location

    def __lt__(self, other):
        # Comparison for priority queue based on f value
        return self.f < other.f

    def __le__(self, other):
        # Less than or equal comparison based on f value
        return self.f <= other.f

    def __hash__(self):
        # Hash based on location
        return hash(self.location)

    def __repr__(self):
        # String representation
        return f"({self.location})"

    def is_goal(self):
        # Check if the current state is the goal state
        return self.location == '1,1'

def h1(state):
    # Heuristic function that always returns zero (Uniform Cost Search)
    return 0

def sld(state):
    # Straight-line distance heuristic to the goal
    x, y = map(int, state.location.split(","))
    return math.hypot(x - 1, y - 1)

def read_mars_graph(filename):
    # Read the Mars map from a file and construct the graph
    graph = Graph()
    nodes = {}
    with open(filename, 'r') as file:
        for line in file:
            node_part, neighbors = line.strip().split(":")
            node_name = node_part.strip()
            neighbor_nodes = neighbors.strip().split()

            # Create or retrieve the node
            if node_name not in nodes:
                nodes[node_name] = Node(node_name)
                graph.add_node(nodes[node_name])

            for neighbor_name in neighbor_nodes:
                # Create or retrieve the neighbor node
                if neighbor_name not in nodes:
                    nodes[neighbor_name] = Node(neighbor_name)
                    graph.add_node(nodes[neighbor_name])

                # Add the edge between the nodes
                graph.add_edge(Edge(nodes[node_name], nodes[neighbor_name], 1))
    return graph

if __name__ == "__main__":
    filename = 'MarsMap'  # Filename of the Mars map
    mars_graph = read_mars_graph(filename)
    start_state = map_state(location="8,8", mars_graph=mars_graph)

    # A* search with straight-line distance heuristic
    result = a_star(start_state, sld, map_state.is_goal)
    if result:
        print("Straight-line distance heuristic:")
        for state in result:
            print(state.location)
    else:
        print("No path found.")

    # A* search with zero heuristic (Uniform Cost Search)
    result = a_star(start_state, h1, map_state.is_goal)
    if result:
        print("Path found by uniform cost search:")
        for state in result:
            print(state.location)
    else:
        print("No path found.")



