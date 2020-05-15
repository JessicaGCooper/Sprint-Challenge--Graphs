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

rooms_visited_inorder = []
rooms_visited = set()
traversal_path = []
graph = {}
for i in range(0, 19):
    graph[i] = {}

def growing_graph(graph):
    for each in player.current_room.get_exits():
        graph[player.current_room.id].update( {each: '?'})
    while '?' in graph[player.current_room.id].values():    
        prior_key = player.current_room.id
        direction = random.choice(list(graph[player.current_room.id]))
        while graph[player.current_room.id][direction] != '?':
            direction = random.choice(list(graph[player.current_room.id]))
        if graph[player.current_room.id][direction] == '?':
            player.travel(direction)
            traversal_path.append(direction)
            rooms_visited_inorder.append(player.current_room.id)
            rooms_visited.add(player.current_room.id)
            graph[prior_key][direction] = player.current_room.id
            if direction == 'n':
                inverse = 's'
            elif direction == 's':
                inverse = 'n'
            elif direction == 'e':
                inverse = 'w'
            elif direction == 'w':
                inverse = 'e'
            for each in player.current_room.get_exits():
                graph[player.current_room.id].update( {each: '?'})
            graph[player.current_room.id][inverse] = prior_key
    return graph

print(growing_graph(graph))
print(traversal_path)
# print(rooms_visited)
# print(rooms_visited_inorder)
print(player.current_room.id)

##function is looping through and populating an adjacency graph as it does so, per this model:
##Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths)

##Need to write the BFT to walk back to the nearest location and outputs a traveseral array to append to current traversal array
##what should be stored in Queue? I believe it will have to be the room_ids
##How to keep track of all paths? I think we can make an array of directions traversed.
##Do I need to keep track of room no? No, player.current_room.id will.
def bfs_backtrack_shortest_path():
    q = Queue()
    possible_exits = graph[player.current_room.id]
    for direction, room_id in possible_exits.items():
        q.enqueue([(room_id, direction)])

    back_track_visited = set()
    back_track_paths = []
    ##while loop needs to loop until: '?' in graph[player.current_room.id].values()
    # while '?' not in graph[player.current_room.id].values():
    if q.size() > 0:
        r = q.dequeue()
        ##check if room_id in last element of r in back_track_visited, if not add to visited ()
        if r[-1][0] not in back_track_visited:
            back_track_visited.add(r[-1])

        ##if '?' present append path to back_track_paths and move on to next item in queue, else append all possible directions:
        if '?' not in graph[player.current_room.id].values():
            back_track_paths.append(r)
            print(f'back_track_paths: {back_track_paths}')
        ##we should be going back through already visited rooms so the directions should be populated alread, use the room_id as key to get direction: room dictionary
        curr_possible_exits = graph[player.current_room.id]
        for direction, room_id in curr_possible_exits.items():
            ##travel in direction only if room not already backtracked to
            for each in back_track_visited:
                if room_id != each[0]:
                    ##create copy of path of room ids represented by r
                    copy = r.copy()
                    player.travel(direction)
                    ##append room_id, direction tuple to copy
                    copy.append((room_id, direction))
    ##find the shortest backtrack       
    shortest_path = back_track_paths[0]
    for path in back_track_paths:
        if len(path) < len(shortest_path):
            shortest_path = path
    return shortest_path

backtrack = bfs_backtrack_shortest_path()
##append new direction to overall traversal list
for each in backtrack:
    traversal_path.append(each[1])
print('updated traversal:')
print(traversal_path)
print(player.current_room.id)
while len(rooms_visited) < 19:
    growing_graph(graph)
    bfs_backtrack_shortest_path()
    backtrack = bfs_backtrack_shortest_path()
    ##append new direction to overall traversal list
    for each in backtrack:
        traversal_path.append(each[1])
    print('updated traversal:')
    print(traversal_path)
    print(player.current_room.id)
print('Final:')
print(rooms_visited)
print(traversal_path)


##Then take the room_id it finds(which will be player.current_room.id so no need to store it) as the starting point to go through the DFT function above

##Then call the BFT function again with the ending room(which will be player.current_room.id so no need to store it) from the DFT as starting point

##loop through these functions until the visited set is the same length as the number or rooms 




# TRAVERSAL TEST - DO NOT MODIFY
# visited_rooms = set()
# player.current_room = world.starting_room
# visited_rooms.add(player.current_room)

# for move in traversal_path:
#     player.travel(move)
#     visited_rooms.add(player.current_room)

# if len(visited_rooms) == len(room_graph):
#     print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
# else:
#     print("TESTS FAILED: INCOMPLETE TRAVERSAL")
#     print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



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
