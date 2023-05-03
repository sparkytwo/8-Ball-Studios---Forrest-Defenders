import pyasge
from game.gamedata import GameData

from queue import PriorityQueue

def \
        pathfind(xy: pyasge.Point2D, ab: pyasge.Point2D, data: GameData):

    '''
    Implementation of A* algorithm, used for finding the shortest path to the player.
    '''
    # convert 2d point to tile location
    current_location = data.game_map.tile(xy)
    tile_location = data.game_map.tile(ab)

    if data.game_map.costs[tile_location[1]][tile_location[0]] == 1:
        return []

    # set the maps bounds
    map_width = data.game_map.width
    map_height = data.game_map.height

    # add player location to queue
    queue = PriorityQueue()
    queue.put((0, current_location))

    # visited tiles
    visited = [current_location]

    # parents used for reconstructing path
    parents = {current_location: None}

    # heuristic function - estimates the distance between two tiles, and guides the search to the target.
    def heuristic(a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    while not queue.empty():
        # next tile to visit
        current = queue.get()[1]
        # check for target pos
        if current == tile_location:
            # reconstruct the path
            path = [tile_location]
            while parents[path[0]] is not None:
                path.insert(0, parents[path[0]])
            tiles_to_visit = [data.game_map.world(tile) for tile in path]
            tiles_to_visit.pop(0)
            return tiles_to_visit

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbour = (current[0] + dx, current[1] + dy)
            # check if the neighbour is within the map bounds
            if (0 <= neighbour[0] < map_width) and (0 <= neighbour[1] < map_height):
                # check if the neighbour has already been visited or has a high cost
                if (neighbour not in visited) and (data.game_map.costs[neighbour[1]][neighbour[0]] == 0):
                    # calculate the cost and add the neighbour to the queue, mark it as visited, and set its parent
                    cost = heuristic(neighbour, tile_location)
                    queue.put((cost, neighbour))
                    visited.append(neighbour)
                    parents[neighbour] = current



    # if we get here, there is no path to the target
    return []

