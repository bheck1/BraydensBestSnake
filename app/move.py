import numpy as np

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

UNOCCUPIED = 1
OCCUPIED   = -1
FOOD       = 1
HEAD       = -2
TAIL       = 4
HEALTHLIM = 25
game_state = ""
directions = {'up': 0, 'down': 0, 'left': 0, 'right': 0}


def calculate_move(board_matrix, game_state):	

    if len(game_state["you"]["body"]) < 8 :
        HEALTHLIM = 100
    else:
        HEALTHLIM = 20
		
    set_game_state(game_state)
    height = game_state["board"]["height"]
    head = game_state['you']["body"][0]
    x = head["x"]
    y = head["y"]
    print("Head:", x, y)
    health = game_state['you']["health"]


    # Check up
    if head["y"] - 1 < 0 or board_matrix[y-1][x] == OCCUPIED :
        directions["up"] = -1000
    else:
        directions["up"] = sum(board_matrix, head["x"], head["y"] - 1, height, game_state)


    # Check down
    if head["y"] + 1 > (height - 1) or board_matrix[y+1][x] == OCCUPIED :
        directions["down"] = -1000
    else:
        directions["down"] = sum(board_matrix, head["x"], head["y"] + 1, height, game_state)


    # Check Left
    if head["x"] - 1 < 0 or board_matrix[y][x-1] == OCCUPIED :
        directions["left"] = -1000
    else:
        directions["left"] = sum(board_matrix, head["x"] - 1, head["y"], height, game_state)


    # check right
    if head["x"] + 1 > (height - 1) or board_matrix[y][x+1]== OCCUPIED :
        directions["right"] = -1000
    else:
        directions["right"] = sum(board_matrix, head["x"] + 1, head["y"], height, game_state)

    if( health < HEALTHLIM and len(game_state['board']['food'])>0):
        find_food(game_state, board_matrix)



    print(max(directions, key=lambda k: directions[k]))
    quad(board_matrix, game_state)
    print("UP", directions["up"])
    print("DOWN", directions["down"])
    print("LEFT", directions["left"])
    print("RIGHT", directions["right"])
    return max(directions, key=lambda k: directions[k])


def sum(matrix, x, y, height, gamestate):
    sum = 0
    if matrix[y ][x] == HEAD:
        snek = get_snek(x, y , game_state)
        if is_bigger(snek, gamestate):
            sum += 0
        else:
            sum += -100
            print(snek)

    if (x - 1) >= 0:
        sum += matrix[y][x-1]
        if matrix[y][x-1] == HEAD :
            snek = get_snek(x-1, y, game_state)
            if is_bigger(snek, gamestate):
                sum += 200
            else:
                sum += -75
                print(snek)

    if (x + 1) < height:
        sum += matrix[y][x+1]
        if matrix[y][x+1] == HEAD :
            snek = get_snek(x+1, y, game_state)
            if(is_bigger(snek, gamestate)):
                sum += 200
            else:
                sum += -75
                print(snek)

    if (y - 1) >= 0:
        sum += matrix[y-1][x]
        if matrix[y-1][x] == HEAD :
            snek = get_snek(x, y-1, game_state)
            if is_bigger(snek, gamestate):
                sum += 200
            else:
                sum += -75
                print(snek)

    if (y + 1) < height:
        sum += matrix[y+1][x]
        if matrix[y+1][x] == HEAD :
            snek = get_snek(x, y+1, game_state)
            if is_bigger(snek, gamestate):
                sum += 200
            else:
                sum += -75
                print(snek)

    if (x-1) >= 0 and (y+1) < height:
        sum += matrix[y+1][x-1]

    if (x-1) >= 0 and (y-1) > 0:
        sum += matrix[y-1][x-1]

    if (x+1)< height and (y+1) < height:
        sum += matrix[y+1][x+1]

    if (x-1) > 0 and (y-1) > 0:
        sum += matrix[y-1][x-1]

    return sum + matrix[y][x]


def find_food(game_state, board_matrix ):
    minsum = 1000
    y = game_state['you']["body"][0]["y"]
    x = game_state['you']["body"][0]["x"]

    for food in game_state["board"]["food"]:
        tot = abs(food['x'] - x)
        tot += abs(food['y'] - y)
        if (tot < minsum):
            goodfood = food
            minsum = tot

    find_path(game_state, board_matrix,x,y, goodfood["x"], goodfood['y'])



def find_path(game_state, board_matrix, x, y, foodx, foody):
    height = game_state["board"]["height"]
    grid = Grid(width=height, height=height, matrix=board_matrix)
    start = grid.node(x, y)
    end = grid.node(foodx, foody)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, runs = finder.find_path(start, end, grid)

    if (len(path) > 0):
        pathx = path[1][0]
        pathy = path[1][1]

        y = game_state['you']["body"][0]["y"]
        x = game_state['you']["body"][0]["x"]
        # go up
        if ((y - 1) == pathy) and (x == pathx):
            directions["up"] += 20
            print("Pick: UP")
        # go down
        if ((y + 1) == pathy) and (x == pathx):
            directions["down"] += 20
            print("Pick: down")
        # go left
        if ((x - 1) == pathx) and (y == pathy):
            directions["left"] += 20
            print("Pick: left")
        # go right
        if ((x + 1) == pathx) and (y == pathy):
            directions["right"] += 20
            print("Pick: right")


def quad(matrix, game_state):
    x =game_state["you"]["body"][0]["x"]
    y = game_state["you"]["body"][0]["y"]
    height = game_state['board']['height']
    quad1 = 0
    quad2 = 0
    quad3 = 0
    quad4 = 0
    for i in range(y):
        for j in range(x):
            if(matrix[j][i]== UNOCCUPIED):
                quad1 += 1

    for i in range(y):
        for j in range(x, height):
            if(matrix[j][i]== UNOCCUPIED):
                quad2 += 1

    for i in range(y, height):
        for j in range(x):
            if(matrix[j][i]== UNOCCUPIED):
                quad3 += 1

    for i in range(y, height):
        for j in range(x, height):
            if(matrix[j][i]== UNOCCUPIED):
                quad4 += 1
    directions['up'] += (quad1 + quad2)/height
    directions['down'] += (quad3 + quad4)/height
    directions['left'] += (quad1 + quad3)/height
    directions['right'] += (quad2 + quad4)/height
    print(quad1, quad2, quad3, quad4)

def is_bigger(snek, game):
    if len(game["you"]["body"]) > snek:
        print("length**************")

        return True
    print("SNake length", snek, "our length ", len(game['you']['body']))
    return False

def get_snek(x, y, game_state):
    for snek in game_state["board"]["snakes"]:
        snake_body = snek['body']
        for xy in snake_body[0:]:
            if( xy["y"]== y and xy["x"]==x):
                return len(snake_body)


def set_game_state(new_game_state):
    global game_state
    game_state = new_game_state


def get_game_State():
    return game_state
