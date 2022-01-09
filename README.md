# OOP Ex4

## About the project

In this project, we programmed a pokemon game which was based on directed weighted graph. The game, was programmed by Python.

## Classes and methods 

The part of the project was based on the previous task. So we used 3 previous classes.

## my_graph

The graph "arena" that the agent goes around and collects pokemon along the way

|Method | Desc. |
|--------------|-------------|
| node_size | returns the number of vertices in the graph |
| edge_size | Returns the number of edges in the graph |
| add_edge | connects between 2 points, src and dest, making an edge with a given weight|
| add_node |  adds a vertex to a graph |
| get_all_v |  return a dictionary containing vertices and their info |
| all_in_edges_of_node | returns a dictionary containing edges sources that go in a given destination |
| all_out_edges_of_node | returns a dictionary containing edges destinations that go out a given source|
| get_mc | returns mod count, which basically is the number of changes that happen upon a graph |
| remove_node |deletes a given node from the graph. |
| remove_edge | deletes an edge within given src and dest |
| add_pokemon | adds a pokemon to the graph's collection of pokemon |
| add_agent | adds an agent to the graph's collection of agents |
| edge_pokemon| using given pos of a pokemon, returns ids of src and dest of the edge on which the pokemon is located|

## GraphAlgo:

contains graph related algorithms

|Method | Desc. |
|--------------|-------------|
| get_graph | returns the graph |
| load_graph_data | loads a graph from given json string |
| load_pokemon  | loads a dict of pokemon from a given json string |
| load_agents  | loads a dict of agents from a given json string |
| shortest_path | calculates the shortest route from given source node and destination node.|
| tsp | calculates for the shortest path to pass between a given list of vertices |
| centerPoint | Calculates the central node, from which the other nodes can be reached in the "cheapest" way. |
| save_graph_json | saves a graph to json (wasn't used) |



 # The game algorithm 
 
 The center and shortest path algorithms were mostly used in the game, more can be learned in our wiki

## Client 
The client class was included in our assignment.
Its functions that connect with the given server. By sending messages to a server it
executes the commands for the game.

|Function name | Explanation |
|--------------|-------------|
| start_connection | start connection with a server |
| send_message | the function that sends messages with commands to a server |
| get_agents | return the agents that are on the graph (returns a json string) |
| add_agent | add an agent to the game that would start on some node|
| get_graph |  returns us a graph of specific case scenario |
| get_info | returns general information about the game |
| get_pokemons | returns pokemons that are in the moment of the game|
| is_running | returns true if the game is still running ,false if not |
| time to end | returns the time to the end of the game |
| start | begins the game |
| stop | stops the game and reports to server |
| stop_connection | stops the connection with the server |
| log_in | allows to log in with id and report about the cases |
| choose_next_edge | choosing the next node the agent will move to |
| move | makes a move for agent |

 
## running the program 
 You can run our algorithm with the release
 
 
