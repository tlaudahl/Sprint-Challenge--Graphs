from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
traversal_path = []

opposites = {'n':'s', 's':'n', 'e':'w', 'w':'e' }

previous_room = [None]
rooms = {}
visited = {}

def check_direction(room_id):
    directions = []
    for item in ['n', 's', 'e', 'w']:
        if item in room_graph[room_id][1].keys():
            directions.append(item)
    return directions

while len(visited) < len(room_graph):
    room_id = player.current_room.id
    if room_id not in rooms:
        visited[room_id] = room_id
        rooms[room_id] = check_direction(room_id)
    
    if len(rooms[room_id]) < 1:
        previous_direction = previous_room.pop()
        traversal_path.append(previous_direction)
        player.travel(previous_direction)
    else:
        next_direction = rooms[room_id].pop()
        traversal_path.append(next_direction)
        previous_room.append(opposites[next_direction])
        player.travel(next_direction)

# TRAVERSAL TEST
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