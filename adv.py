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
map_file = "maps/test_loop_fork_copy.txt"
# map_file = "maps/main_maze.txt"

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
print(rooms_visited)
print(rooms_visited_inorder)
print(player.current_room.id)
# 
# direction = None
# if direction == None:
#     direction = random.choice(list(graph[player.current_room.id]))
#     if graph[player.current_room.id][direction] == '?':
#         player.travel(direction)
#         graph[prior_key][direction] = player.current_room.id
#         if direction == 'n':
#             inverse = 's'
#         elif direction == 's':
#             inverse = 'n'
#         elif direction == 'e':
#             inverse = 'w'
#         elif direction == 'w':
#             inverse = 'e'
#         graph[player.current_room.id] = {}
#         for each in player.current_room.get_exits():
#             graph[player.current_room.id].update( {each: '?'})
#         graph[player.current_room.id][inverse] = prior_key
# print(graph)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# Initial Room ID is 0


p = Stack()
##place exits array for current room in variable
exits = player.current_room.get_exits()
##place current room id in shorter variable
room_id = player.current_room.id
# print(player.current_room.get_exits())
# print(player.current_room.id)
# for direct in exits:
#     p.push(direct)

# while p.size() > 0:

#     ##pop the most recent room added
#     r = p.pop()

#     ##add to visited
#     rooms_visited.add(player.current_room.id)
#     traversal_path.append(r)
#     rooms_as_visited.append(player.current_room.id)
#     player.travel(r)
#     ##place exits array for current room in variable
#     curr_exits = player.current_room.get_exits()
#     ##place current room id in shorter variable
#     curr_room_id = player.current_room.id
#     ##for each direction in exits add a tuple with room num and the direction to stack
#     for room in curr_exits:
#         p.push(room)
                
# print('Rooms:')
# print(rooms_visited)
# print(len(rooms_visited))
# print('traversal_path:')
# print(traversal_path)
# print(len(traversal_path))                   


    




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
