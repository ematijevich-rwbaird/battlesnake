# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import math
#afsdfsdf
# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    #print("INFO")

    return {
        "apiversion": "1",
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

    f = open("lastmove.txt", "r", encoding='utf-8')
    last_move = f.readline()
    f.close()
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
        #print("1")

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
        #print("2")
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
        #print("3")
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False
        #print("4")

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    if my_head['x'] == board_width - 1 :
        is_move_safe["right"] = False
        #print("5")
    if my_head['x'] == 0 :
        is_move_safe["left"] = False
        #print("6")
    if my_head['y'] == board_height - 1 :
        is_move_safe["up"] = False
        #print("7")
    if my_head['y'] == 0 :
        is_move_safe["down"] = False
        #print("8")

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
  


    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    
    for op in opponents :
            if is_move_safe["right"] :
                for piece in op['body']:
                    if my_head['x'] == piece['x'] - 1 and my_head['y'] == piece['y']:
                        is_move_safe['right'] = False
                        #print('9')
                        break
            if is_move_safe["left"] :
                for piece in op['body']:
                    if my_head['x'] == piece['x'] + 1 and my_head['y'] == piece['y']:
                        is_move_safe['left'] = False
                        #print('10')
                        break
            if is_move_safe["up"] :
                for piece in op['body']:
                    if my_head['y'] == piece['y'] - 1 and my_head['x'] == piece['x']:
                        is_move_safe['up'] = False
                        #print('11')
                        break
            if is_move_safe["down"] :
                for piece in op['body']:
                    if my_head['y'] == piece['y'] + 1 and my_head['x'] == piece['x']:
                        is_move_safe['down'] = False
                        #print("12")
                        break


    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)
    

    #print(safe_moves)
    if len(safe_moves) == 0:
        #print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # Choose a random move from the safe ones
    
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    foods = game_state['board']['food']
    
    next_move = []
    #find closest food
    if len(foods) != 0 :
        best_food = foods[0]
        best_distance = math.sqrt(pow(my_head['x'] - foods[0]['x'], 2) + pow(my_head['y']  - foods[0]['y'], 2))
        for food in foods :
            distance = math.sqrt(pow(my_head['x'] - food['x'], 2) + pow(my_head['y']  - food['y'], 2))
            if distance < best_distance :
                best_food = food

        
        x_distance = abs(my_head['x'] - best_food['x'])
        y_distance = abs(my_head['y'] - best_food['y'])
        
        x_or_y = min(x_distance, y_distance)

        # print("Best food: ",best_food,"x_distance: ",x_distance,", y_distance: ", y_distance)
        if x_distance == x_or_y :
            if my_head['y'] - best_food['y'] < 0 and is_move_safe['up']:
                next_move = 'up'
            elif my_head['y'] - best_food['y'] > 0 and is_move_safe['down']:
                next_move = "down"
        elif y_distance == x_or_y :
            if my_head['x'] - best_food['x'] > 0  and is_move_safe['left']:
                next_move = "left"
            elif my_head['x'] - best_food['x'] < 0 and is_move_safe['right']:
                next_move = "right"
        else:
            if last_move is not None :
                next_move = last_move
            
    
    if len(next_move) == 0 :
        next_move = random.choice(safe_moves)


    #print(f"MOVE {game_state['turn']}: {next_move}")
    f = open("lastmove.txt", "w", encoding='utf-8')
    f.write(next_move)
    f.close()
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})
    