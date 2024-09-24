from copy import deepcopy
from search_algorithms import (
    breadth_first_search,
    depth_first_search,
    depth_limited_search,
)

class RoverState:
    def __init__(self, loc="station", sample_extracted=False, holding_sample=False, charged=False, holding_tool=False):
        # Initialize the rover's state with default values
        self.loc = loc  # Current location of the rover
        self.sample_extracted = sample_extracted  # Whether the sample has been extracted
        self.holding_sample = holding_sample  # Whether the rover is holding the sample
        self.charged = charged  # Whether the rover is charged
        self.holding_tool = holding_tool  # Whether the rover is holding the tool
        self.prev = None  # Reference to the previous state

    def __eq__(self, other):
        # Check if two states are equal based on their attributes
        return (
            self.loc == other.loc
            and self.sample_extracted == other.sample_extracted
            and self.holding_sample == other.holding_sample
            and self.charged == other.charged
            and self.holding_tool == other.holding_tool
        )

    def __hash__(self):
        # Compute a hash value for the state (needed for sets and dictionaries)
        return hash((
            self.loc,
            self.sample_extracted,
            self.holding_sample,
            self.charged,
            self.holding_tool,
        ))

    def __repr__(self):
        # Return a string representation of the state
        return (
            f"Location: {self.loc}\n"
            f"Sample Extracted?: {self.sample_extracted}\n"
            f"Holding Sample?: {self.holding_sample}\n"
            f"Holding Tool?: {self.holding_tool}\n"
            f"Charged? {self.charged}"
        )

    def successors(self, action_list):
        # Generate successor states based on available actions
        successors = []
        for action in action_list:
            new_state = action(self)
            if new_state != self:
                successors.append((new_state, action.__name__))
        return successors

# Actions

def move_to_sample(state):
    # Move the rover to the sample location if it's not already there
    if state.loc != "sample":
        new_state = deepcopy(state)
        new_state.loc = "sample"
        new_state.prev = state
        return new_state
    return state  # No change if already at sample location

def move_to_station(state):
    # Move the rover to the station if it's not already there
    if state.loc != "station":
        new_state = deepcopy(state)
        new_state.loc = "station"
        new_state.prev = state
        return new_state
    return state  # No change if already at station

def move_to_battery(state):
    # Move the rover to the battery location if it's not already there
    if state.loc != "battery":
        new_state = deepcopy(state)
        new_state.loc = "battery"
        new_state.prev = state
        return new_state
    return state  # No change if already at battery

def pick_up_sample(state):
    # Have the rover pick up the sample if it's extracted, at sample location, and not already holding it
    if state.sample_extracted and state.loc == "sample" and not state.holding_sample:
        new_state = deepcopy(state)
        new_state.holding_sample = True
        new_state.prev = state
        return new_state
    return state  # No change if conditions not met

def drop_sample(state):
    # Have the rover drop the sample if it's holding it and at the station
    if state.holding_sample and state.loc == "station":
        new_state = deepcopy(state)
        new_state.holding_sample = False
        new_state.prev = state
        return new_state
    return state  # No change if conditions not met

def charge(state):
    # Charge the rover if it's at the battery location and not already charged
    if state.loc == "battery" and not state.charged:
        new_state = deepcopy(state)
        new_state.charged = True
        new_state.prev = state
        return new_state
    return state  # No change if conditions not met

def pick_up_tool(state):
    # Have the rover pick up the tool if it's at the station and not already holding it
    if state.loc == "station" and not state.holding_tool:
        new_state = deepcopy(state)
        new_state.holding_tool = True
        new_state.prev = state
        return new_state
    return state  # No change if conditions not met

def drop_tool(state):
    # Have the rover drop the tool if it's holding it and at the sample location
    if state.holding_tool and state.loc == "sample":
        new_state = deepcopy(state)
        new_state.holding_tool = False
        new_state.prev = state
        return new_state
    return state  # No change if conditions not met

def use_tool(state):
    # Have the rover use the tool to extract the sample if conditions are met
    if state.holding_tool and state.loc == "sample" and not state.sample_extracted:
        new_state = deepcopy(state)
        new_state.sample_extracted = True
        new_state.prev = state
        return new_state
    return state  # No change if conditions not met

# Action lists
# Part 3 (without tool requirement)
action_list_part3 = [
    move_to_sample,
    pick_up_sample,
    move_to_station,
    drop_sample,
    move_to_battery,
    charge,
]

# Part 5 and 6 (with tool requirement)
action_list = [
    pick_up_tool,
    move_to_sample,
    use_tool,
    drop_tool,
    pick_up_sample,
    move_to_station,
    drop_sample,
    move_to_battery,
    charge,
]

# Goal functions

def mission_complete(state):
    # Define when the mission is complete
    return (
        state.loc == "battery"
        and state.charged
        and not state.holding_sample
        and state.sample_extracted
    )

def move_to_sample_goal(state):
    # Goal is to move to sample location
    return state.loc == "sample"

def remove_sample_goal(state):
    # Goal is to have extracted the sample and be holding it
    return state.sample_extracted and state.holding_sample

def return_to_charger_goal(state):
    # Goal is to return to battery and be charged
    return state.loc == "battery" and state.charged

if __name__ == "__main__":
    # Part 3: Simple Problem
    initial_state_part3 = RoverState()
    print("Part 3)")
    # BFS
    bfs_result = breadth_first_search(
        initial_state_part3, action_list_part3, mission_complete
    )
    print(f"BFS: count = {bfs_result[2]}")

    # DFS
    dfs_result = depth_first_search(
        initial_state_part3, action_list_part3, mission_complete
    )
    print(f"DFS: count = {dfs_result[2]}")

    # Part 5: Problem with Tool Requirement
    initial_state = RoverState()
    print("\nPart 5)")
    # BFS
    bfs_result = breadth_first_search(initial_state, action_list, mission_complete)
    print(f"BFS: count = {bfs_result[2]}")

    # DFS
    dfs_result = depth_first_search(initial_state, action_list, mission_complete)
    print(f"DFS: count = {dfs_result[2]}")

    # DLS with limit = 17
    limit = 17
    dls_result = depth_limited_search(
        initial_state, action_list, mission_complete, limit
    )
    print(f"DLS: ran with limit = {limit}, count = {dls_result[2]}")

    # Part 6: Problem Decomposition
    print("\nPart 6)")
    # Using BFS
    print("Using BFS:")
    # Subproblem 1: moveToSample
    result1 = breadth_first_search(initial_state, action_list, move_to_sample_goal)
    print(f"moveToSample: count = {result1[2]}")
    # Subproblem 2: removeSample
    result2 = breadth_first_search(result1[0], action_list, remove_sample_goal)
    print(f"removeSample: count = {result2[2]}")
    # Subproblem 3: returnToCharger
    result3 = breadth_first_search(result2[0], action_list, return_to_charger_goal)
    print(f"returnToCharger: count = {result3[2]}")

    # Using DFS
    print("\nUsing DFS:")
    # Subproblem 1: moveToSample
    result1_dfs = depth_first_search(initial_state, action_list, move_to_sample_goal)
    print(f"moveToSample: count = {result1_dfs[2]}")
    # Subproblem 2: removeSample
    result2_dfs = depth_first_search(result1_dfs[0], action_list, remove_sample_goal)
    print(f"removeSample: count = {result2_dfs[2]}")
    # Subproblem 3: returnToCharger
    result3_dfs = depth_first_search(
        result2_dfs[0], action_list, return_to_charger_goal
    )
    print(f"returnToCharger: count = {result3_dfs[2]}")

    # Using DLS
    print("\nUsing DLS:")
    limit = 17
    # Subproblem 1: moveToSample
    result1_dls = depth_limited_search(
        initial_state, action_list, move_to_sample_goal, limit
    )
    print(f"moveToSample: count = {result1_dls[2]}")
    # Subproblem 2: removeSample
    result2_dls = depth_limited_search(
        result1_dls[0], action_list, remove_sample_goal, limit
    )
    print(f"removeSample: count = {result2_dls[2]}")
    # Subproblem 3: returnToCharger
    result3_dls = depth_limited_search(
        result2_dls[0], action_list, return_to_charger_goal, limit
    )
    print(f"returnToCharger: count = {result3_dls[2]}")





