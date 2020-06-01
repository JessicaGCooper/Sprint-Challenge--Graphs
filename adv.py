from room import Room
from player import Player
from world import World
from util import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/test_loop_fork_copy.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

"""BEGIN MY CODE"""

#initialize rooms_visited set which contains no duplicates but will make sure all rooms are visited
rooms_visited = set()
#initialize rooms_visited_inorder which allows to see full path and debug by seeing if unnecessary paths are taken
rooms_visited_inorder = [0]
##initialize traversal_path
traversal_path = []
##initialize graph in dictionary format with keys representing all the room numbers in map being used.  
graph = {}
for i in range(0, 500):
    graph[i] = {}

##below function is looping through and populating an adjacency graph as it does so, per this model:
##Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. Until you reach a dead-end (i.e. a room with no unexplored paths)
def growing_graph(graph):
    ##So as not to reset any visite room the below if statement is in place
    if player.current_room.id not in rooms_visited:
        rooms_visited.add(player.current_room.id)
        for each in player.current_room.get_exits():
            graph[player.current_room.id].update( {each: '?'})
    ##until I get to a dead end with no ? this loop will continue then I have to backtrack via the bfs
    while '?' in graph[player.current_room.id].values():
        ##put current room_id in temporary variable to use later when giving value to direction in the room the player moves to    
        prior_key = player.current_room.id
        ##find a random unexplored direction for the player to move to 
        direction = random.choice(list(graph[player.current_room.id]))
        ##make sure the random selection is unexplored (value = '?')
        while graph[player.current_room.id][direction] != '?':
            direction = random.choice(list(graph[player.current_room.id]))
        if graph[player.current_room.id][direction] == '?':
            ##move player in unexplored direction
            player.travel(direction)
            ##replace '?' for that direction with appropriate room_id after player moves
            graph[prior_key][direction] = player.current_room.id
            ##define the inverse of the direction the player moved to use to replace the '?' for the direction the player came from
            if direction == 'n':
                inverse = 's'
            elif direction == 's':
                inverse = 'n'
            elif direction == 'e':
                inverse = 'w'
            elif direction == 'w':
                inverse = 'e'
            ##So as not to reset any visited room the below if statement is in place
            if player.current_room.id not in rooms_visited:
                ##this initializes an empty room with it's available exits although where those exits go is unknown except for the direction the player just came from
                for each in player.current_room.get_exits():
                    graph[player.current_room.id].update( {each: '?'})
            ##populate all necessary sets, arrays
            traversal_path.append(direction)
            rooms_visited_inorder.append(player.current_room.id)
            rooms_visited.add(player.current_room.id)
            ##set the direction the player just came from (in current room) to prior room's id number.
            graph[player.current_room.id][inverse] = prior_key
    ##Function returns adjaceny graph which will be populated in full by the end of adv.py file
    return graph

###BFS function that finds the backtrack path to the last room visited with '?' in it.  Outputs an array of rooms visited while backtracking.
def bfs_backtrack_shortest_path():
    q = Queue()
    ##initialize a path in the queue which begins with room the player is currently in
    q.enqueue([player.current_room.id])
    ##loop until a path is found back to a room with unexplored directions
    while q.size() > 0:
        ##r is an array of room ids, we want to examine the last room id added
        r = q.dequeue()

        ####GENERAL_NOTE:  graph[r[-1]] will be the dictionary of directions and rooms for the key of room_id which is the last room_id in r, the array of room_ids for backtracking we are currently assessing.
        ####
        
        ##if '?' present in directions available to new current room this is first path we have found and will be one of the shortest due to this being a BFS, so we just want to break the while loop and return this path:
        if '?' in graph[r[-1]].values():
            short_path = r
            break
        else:
            curr_possible_exits = graph[r[-1]]
            for direction, room_id in curr_possible_exits.items():
                ##if r is greater than one, there is a need to exclude r[-2] which will be the room visited just before the last room in r.  We don't want to create a path that includes going back to the room we just came from.
                if len(r) > 1:
                    if room_id != r[-2]:
                        copy = r.copy()
                        # append room_id to copy
                        copy.append(room_id)
                        # enqueue copy with new room_id added
                        q.enqueue(copy)
                ##else r is just one in length, in that case we have to go back to the last room to backtrack, (there SHOULD be only one possible exit if r is one)
                else:
                    copy = r.copy()
                    # append room_id to copy
                    copy.append(room_id)
                    # enqueue copy with new room_id added
                    q.enqueue(copy)
    return short_path

##call backtrack function and return it's the resulting array as 'backtrack'
backtrack = bfs_backtrack_shortest_path()
##convert backtrack into directions
directions = []
for i in range(0, len(backtrack)-1):
    ##options will be the possible exits dictionary for the room_id in backtrack
    options = graph[backtrack[i]]
    print(options)
    ##key is direction, value is room number
    ##if the room number in the possible exits/options dictionary is equal to next room number in the backtrack array we know this is the way we went, then to convert to directions we take key/direction and append to directions array
    for key, value in options.items():
        if value == backtrack[i+1]:
            directions.append(key)
for move in directions:
    ##while building the directions array to add to traversal list we will also move the player this way so that the current room id will be current when the growing_graph function is called
    player.travel(move)
    ###rooms_visited_inorder is used to debug since I can tell if routes are taken when they should not be
    rooms_visited_inorder.append(player.current_room.id)

##after completing the directions array as a result of the backtrack we add those directions to the traversal_path
traversal_path.extend(directions)
## now we call growing_graph again for the next DFT until it hits a deadend
growing_graph(graph)

##Now we will loop through all of the above described continuously until the the length of the rooms_visited set is equal to the number of rooms in the map
while len(rooms_visited) < 500:
    ##call bft_backtrack function (note the graph has already been initiliazed and the function for that DFT run twice before this loop is even begun)
    backtrack = bfs_backtrack_shortest_path()
    ##convert backtrack into directions
    directions = []
    for i in range(0, len(backtrack)-1):
        ##options will be the possible exits dictionary for the room_id in backtrack
        options = graph[backtrack[i]]
        ##key is direction, value is room number
        for key, value in options.items():
            if value == backtrack[i+1]:
                directions.append(key)
    ##player moves through backtrack path
    for move in directions:
        player.travel(move)
        rooms_visited_inorder.append(player.current_room.id)
    traversal_path.extend(directions)
    ##growing_graph called again now that a room with '?' still in it has been found by backtrack function
    growing_graph(graph)

print('FINAL RESULTS:')
print(f'rooms_visited: {rooms_visited}')
print(f'length of traversal path: {len(traversal_path)}')
print(f'room player is in when traversal ends: {player.current_room.id}')

"""END MY CODE"""


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
