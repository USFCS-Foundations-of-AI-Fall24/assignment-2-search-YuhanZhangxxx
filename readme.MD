### Assignment 2: Search
#### Due Friday Sept 20 at 11:59pm. 

Note: For the programming  portions of the assignment, please provide a file called submission.py that demos your code.
For the written portions, please prepare a document called assignment2.pdf and put your answers in there.
And don't forget to put your name on your assignment!

**On time management!** This assignment has many small components; the key to success will be starting early.
I've added suggested milestones _in italics_. 

_Sept 7: read through assignment. Identify any initial questions._

**Question 1. (10 points)**
_Sept 9._

Fill in the following table in a separate PDF document.

| Algorithm  | Time Complexity  | Space Complexity  | Complete?  | Optimal?  |
|---|---|---|---|---|
| BFS  |   |   |   |   |
| UCS  |   |   |   |   |
| DFS   |   |   |   |   |
| DLS  |   |   |   |   |
| IDS |    |   |   |   |
|A*  |    |    |   |   |

**Question 2** 

One of the first applications of search was in robot planning. In this setting, we define a state, a goal, and a set 
of actions. Our actions transform the state, creating a search space. We can then apply our classic search
algorithms to this problem.

We'll start with a simple version of the Mars Rover problem. This can be found in mars_planner.py. 
I've also included some unit tests to help you get things working. In later assignments, I'll ask you to build 
your own unit tests.

There are three locations: the station, the sample site, and the charger.
Our rover should travel from the station to the sample, extract the sample, pick the sample up,
bring the sample back to the station, and then go to the charger to recharge. 

It will do this by finding a series of *actions* to take. Those actions should lead us to a state that satisfies the *goal*.

In this case, our state has four variables, indicating location, sample state,  
whether we're holding the sample, and whether we're charged. (there's also a pointer to the previous state.)

We also have a set of actions. Each action is implemented as a function that can be applied to a state.
This approach allows us a great deal of flexibility to solve a variety of problems and easily add or change 
our actions without breaking our existing code.

1. **(5 points)**. _Sept 10_ We need an __eq__ function in RoverState to detect repeated states. Implement this. 
Two states are equal if all of their instance variables are equal.

2. **(5 points)** _Sept 11_ Now we need to create a *goal function*. This is a function that will return True if a state is the goal state,
and False otherwise. I've provided a battery_goal test that returns True if we are at the battery and False otherwise.

Create a mission_complete goal function that returns True if we are at the battery, charged, and the sample is at the station.

3. **(5 points)** _Sept 12_ Run this with the included BFS and DFS implementations. Extend each of these to count the number of states generated. 
Print this out at the end.

4. **(10 points)** _Sept 13_ Extend the depth_first_search function to implement *depth_limited_search* by providing an optional *limit* parameter. 
When you are generating successors, only go to depth=limit in the search tree. (You are welcome to extend the RoverState class 
to make this easier if you'd like.) 

5. **(10 points)** _Sept 14_ We found out that the rover cannot extract the sample on its own; it needs a tool. Extend the program as follows: 

Add a holding_tool instance variable to RoverState. Update your constructor and eq methods correctly.
add the following actions: 
-   pick_up_tool 
- drop_tool 
- use_tool. 

Pick_up_tool should return a new state with the holding_tool 
variable set to True, drop_tool should return a new state with the holding_tool variable set to false, and use_tool should 
return a new state with the sample_extracted variable set to True.

Run each of the four algorithms (breadth_first_search, depth_first_search, depth_limited_search, iterative_deepening_search) 
on this new problem and count the number of states generated. 

6. **(10 points)** _Sept 15_ An early insight in solving search-based problems was the idea of *problem decomposition*. If a 
problem can be subdivided into into smaller components that can be solved separately, we can deal with scaling more easily.

Modify your search code so that it instead solves three subproblems: moveToSample, removeSample, and returnToCharger.
You can do this by changing the start state and goal test. How does this change the number of states generated? 

Please add a PDF to your repo with the state data for each of the questions above.

**Question 3** 

For this problem, we will solve a classic path-finding problem using A*. This can be found in routefinder.py

We need to find a route for our rover to find its way from the sample site back to the charger. 
Fortunately, we have a map that we can use to find our way. 
There's a picture of it in the marsmap.docx file; the red cells are areas we cannot travel in.

This data is also captured in the MarsMap file.

You will need to:

a) **(5 points)** _Sept 14_ Complete the read_mars_graph() method so that you can create a graph. 
I've provided a Graph class for you; if you want to modify it, feel free. 

b) **(15 points)** _Sept 17_ In search_algorithms.py, complete the a_star function. 
You will need to implement a straight-line distance heuristic. 
This should compute SLD(p1) = sqrt((p1.x - p2.x)^2 + (p1.y - p2.y)^2)) where p2=(1,1)

SLD should be a separate function that is provided to a_star, NOT something encoded within the algorithm. 
You should be able to pass in a different heuristic function, such as h1, which always returns 0, without changing your code.

c) **(5 points)** _Sept 18_ Run both A* and uniform cost search (i.e. using h1: h=0 for all states) 
on the MarsMap and count the number of states generated. Add this to your results.

**Question 4: Constraints.**

For this question, you'll be using the [(OR-Tools)](https://developers.google.com/optimization) toolkit to help out our Mars rover.
I've provided some sample code for you to use in mapcoloring.py as a starting point that solves
the Bay Area map coloring problem.

This provides our first introduction to *knowledge-based programming*. This is a style of program design
where the focus is on representing complex problem knowledge (constraints in this case) and then handing that
knowledge to an automated solver to find a solution. 

a. **(10 points)** _Sept 19_ Our rover needs to set up nine wireless antennae so that its sensors can collect data and send it back. 
Antennae that are close to each other need to operate on different frequencies so that they don't interfere with each other.

Our rover has three possible frequencies (f1, f2 and f3) that it can assign to an antenna.

It knows that:
- Antenna 1 is adjacent to 2,3 and 4.
- Antenna 2 is adjacent to 1, 3, 5, and 6
- Antenna 3 is adjacent to 1, 2, 6, and 9
- Antenna 4 is adjacent to 1, 2, and 5.
- Antenna 5 is adjacent to 2 and 4
- Antenna 6 is adjacent to 2, 7 and 8
- Antenna 7 is adjacent to 6 and 8
- Antenna 8 is adjacent to 7 and 9
- Antenna 9 is adjacent to 3 and 8

(observant readers will note that this is a variant of the map coloring problem.)

Using the map coloring code as an example, use OR-tools to find an assignment of frequencies to antennae that maintains the constraint that
no adjacent antennae share a frequency.


**Question 5: Deep Blue vs AlphaZero (10 points)**
_Sept 20_

In the late 90s, Deep Blue shocked the world by becoming the first computer to beat a human grandmaster, Garry Kasparov. 
[This paper](https://www.sciencedirect.com/science/article/pii/S0004370201001291?ref=pdf_download&fr=RR-2&rr=851930c31a9617ea) 
describes how Deep Blue was constructed - it took advantage of specialized hardware, 
along with hand-crafted heuristics and many optimizations of the alpha-beta pruning technique we've learned about.

20 years later, the Google team has re-revolutionized game search with the development of AlphaZero, 
which is described [in this paper](https://arxiv.org/pdf/1712.01815.pdf).

AlphaZero uses a very different approach - specifically, a deep neural network is used to learn heuristic functions 
through self-play. (We'll look at reinforcement learning later in the semester). This allows the program to learn to 
play any game, as long as it knows the state space, a goal function, and the legal actions.

These articles are both pretty dense, and I don't expect you to grasp every nuance, but you should be able to read the 
introductions and get the gist of things.

In your written answers, please address the following questions: 

a) What were the engineering advances that led to Deep Blue's success? Which of them can be transferred to other problems, 
and which are specific to chess?

b) AlphaZero is compared to a number of modern game-playing programs, such as StockFish, which work similarly to Deep Blue. 
The paper shows that AlphaZero is able to defeat StockFish even when it is given only 1/100 of the computing time. 
Why is that? Please frame your answer in terms of search and the number of nodes evaluated.


 