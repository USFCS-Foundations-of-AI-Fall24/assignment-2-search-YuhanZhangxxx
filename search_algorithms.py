from collections import deque
from queue import PriorityQueue

# Breadth-First Search (BFS)
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True):
    search_queue = deque()  # Initialize the queue for BFS
    closed_list = set()  # A set to track visited states (closed list)
    state_counter = 0  # Initialize state counter

    # Append the initial state to the search queue
    search_queue.append((startState, ""))
    if use_closed_list:
        closed_list.add(startState)  # Mark the initial state as visited

    while search_queue:
        next_state = search_queue.popleft()  # Dequeue the first state

        # Check if the current state satisfies the goal condition
        if goal_test(next_state[0]):
            # Return the result and state count
            return (next_state[0], next_state[1], state_counter)
        else:
            # Get the successors of the current state
            successors = next_state[0].successors(action_list)

            # Filter out the states that have already been visited
            if use_closed_list:
                successors = [item for item in successors if item[0] not in closed_list]

            # Add the new states to the closed list
            for s in successors:
                closed_list.add(s[0])

            # Update the state counter with the number of successors
            state_counter += len(successors)

            # Add the successors to the search queue
            search_queue.extend(successors)

    # If the goal is not found, return None and the total number of states generated
    return (None, None, state_counter)


# Depth-First Search (DFS)
def depth_first_search(startState, action_list, goal_test, use_closed_list=True, limit=None):
    search_stack = deque()  # Initialize the stack for DFS
    closed_list = set()  # A set to track visited states
    state_counter = 0  # Initialize state counter

    # Append the initial state to the search stack
    search_stack.append((startState, "", 0))  # (state, action, depth)
    if use_closed_list:
        closed_list.add(startState)  # Mark the initial state as visited

    while search_stack:
        next_state, action, depth = search_stack.pop()  # Pop the last state

        # Check if the current state satisfies the goal condition
        if goal_test(next_state):
            # Return the result and state count
            return (next_state, action, state_counter)
        elif limit is None or depth < limit:
            # Get the successors of the current state
            successors = next_state.successors(action_list)

            # Filter out the states that have already been visited
            if use_closed_list:
                successors = [s for s in successors if s[0] not in closed_list]

            # Add the new states to the closed list
            for s in successors:
                closed_list.add(s[0])

            # Update the state counter with the number of successors
            state_counter += len(successors)

            # Add successors to the stack with incremented depth
            for s in successors:
                search_stack.append((s[0], s[1], depth + 1))

    # If the goal is not found, return None and the total number of states generated
    return (None, None, state_counter)


# Depth-Limited Search (DLS)
def depth_limited_search(startState, action_list, goal_test, limit, use_closed_list=True):
    return depth_first_search(startState, action_list, goal_test, use_closed_list, limit)


# Iterative Deepening Search (IDS)
def iterative_deepening_search(startState, action_list, goal_test, max_depth, use_closed_list=True):
    total_state_count = 0  # Initialize total state counter

    for depth in range(max_depth + 1):
        result = depth_limited_search(startState, action_list, goal_test, depth, use_closed_list)
        total_state_count += result[2]  # Accumulate state counts

        if result[0]:
            # Return the result and total state count
            return (result[0], result[1], total_state_count)

    # If the goal is not found, return None and the total number of states generated
    return (None, None, total_state_count)




