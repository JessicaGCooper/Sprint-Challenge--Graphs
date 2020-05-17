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

rooms_visited_inorder = [0]
rooms_visited = set()

traversal_path = []
graph = {}
for i in range(0, 500):
    graph[i] = {}

def growing_graph(graph):
    ##So as not to reset any visite room the below if statement is in place
    if player.current_room.id not in rooms_visited:
        rooms_visited.add(player.current_room.id)
        for each in player.current_room.get_exits():
            graph[player.current_room.id].update( {each: '?'})
    ##until I get to a dead end with no ? this loop will continue then I have to backtrack via the bfs
    while '?' in graph[player.current_room.id].values():    
        prior_key = player.current_room.id
        direction = random.choice(list(graph[player.current_room.id]))
        while graph[player.current_room.id][direction] != '?':
            direction = random.choice(list(graph[player.current_room.id]))
        if graph[player.current_room.id][direction] == '?':
            player.travel(direction)
            graph[prior_key][direction] = player.current_room.id
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
                for each in player.current_room.get_exits():
                    graph[player.current_room.id].update( {each: '?'})
            traversal_path.append(direction)
            rooms_visited_inorder.append(player.current_room.id)
            rooms_visited.add(player.current_room.id)
            graph[player.current_room.id][inverse] = prior_key
    return graph

print(growing_graph(graph))
print(traversal_path)
# print(rooms_visited)
# print(rooms_visited_inorder)
print(player.current_room.id)
print("Rooms visited after graph traversal:")
print(rooms_visited_inorder)
##function is looping through and populating an adjacency graph as it does so, per this model:
##Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths)

##Need to write the BFT to walk back to the nearest location and outputs a traveseral array to append to current traversal array
##what should be stored in Queue? I believe it will have to be the room_ids
##How to keep track of all paths? I think we can make an array of directions traversed.
##Do I need to keep track of room no? No, player.current_room.id will.

def bfs_backtrack_shortest_path():
    q = Queue()
    
    q.enqueue([player.current_room.id])

    # short_path = []

    ##while loop needs to loop until: '?' in graph[player.current_room.id].values()
    # while '?' not in graph[player.current_room.id].values():
    while q.size() > 0:
        ##r is an array of room ids, we want to examine the last room id added
        r = q.dequeue()

        ##if '?' present in directions available to new current room this is first path we have found and will be one of the shortest due to this being a bfs, so we just want to break the while loop and return this path:
        if '?' in graph[r[-1]].values():
            # r.append[player.current_room.id]
            short_path = r
            break
        else:
            
            curr_possible_exits = graph[r[-1]]
            for direction, room_id in curr_possible_exits.items():
                if len(r) > 1:
                    if room_id != r[-2]:
                        copy = r.copy()
                        # append room_id to copy
                        copy.append(room_id)
                        q.enqueue(copy)
                else:
                    copy = r.copy()
                    # append room_id to copy
                    copy.append(room_id)
                    q.enqueue(copy)
    return short_path

backtrack = bfs_backtrack_shortest_path()
##convert backtrack into directions
directions = []
for i in range(0, len(backtrack)-1):
    ##options will be the possible exits dictionary for the room_id in backtrack
    options = graph[backtrack[i]]
    print(options)
    ##key is direction, value is room number
    for key, value in options.items():
        if value == backtrack[i+1]:
            directions.append(key)
for move in directions:
    player.travel(move)
    rooms_visited_inorder.append(player.current_room.id)

traversal_path.extend(directions)

growing_graph(graph)


while len(rooms_visited) < 500:

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
    for move in directions:
        player.travel(move)
        rooms_visited_inorder.append(player.current_room.id)
    # print("Rooms visited after adding backtrack:")
    # print(rooms_visited_inorder)
    traversal_path.extend(directions)
    growing_graph(graph)
    # print("Rooms visited after graph traversal:")
    # print(rooms_visited_inorder)


print('Final:')
print(rooms_visited)
print(len(traversal_path))
print(player.current_room.id)


##Then take the room_id it finds(which will be player.current_room.id so no need to store it) as the starting point to go through the DFT function above

##Then call the BFT function again with the ending room(which will be player.current_room.id so no need to store it) from the DFT as starting point

##loop through these functions until the visited set is the same length as the number or rooms 




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
