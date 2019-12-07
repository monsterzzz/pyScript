import turtle
import random

# This dictionary contains the blocks' information
# Each block type (I, J, L, S, Z, O and T) contains its color and
# tile arrangements of different orientations
blocks = {
    "I": {
        "color": "cyan",
        "tiles":
            [[[1, 0, 0, 0],
              [1, 0, 0, 0],
              [1, 0, 0, 0],
              [1, 0, 0, 0]],

             [[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [1, 1, 1, 1]]]
    },
    "J": {
        "color": "blue",
        "tiles":
            [[[0, 1, 0],
              [0, 1, 0],
              [1, 1, 0]],

             [[0, 0, 0],
              [1, 1, 1],
              [0, 0, 1]],

             [[1, 1, 0],
              [1, 0, 0],
              [1, 0, 0]],

             [[0, 0, 0],
              [1, 0, 0],
              [1, 1, 1]]]
    },
    "L": {
        "color": "orange",
        "tiles":
            [[[1, 0, 0],
              [1, 0, 0],
              [1, 1, 0]],

             [[0, 0, 0],
              [0, 0, 1],
              [1, 1, 1]],

             [[0, 1, 1],
              [0, 0, 1],
              [0, 0, 1]],

             [[0, 0, 0],
              [1, 1, 1],
              [1, 0, 0]]]
    },
    "S": {
        "color": "lime",
        "tiles":
            [[[0, 0, 0],
              [0, 1, 1],
              [1, 1, 0]],

             [[1, 0, 0],
              [1, 1, 0],
              [0, 1, 0]]]
    },
    "Z": {
        "color": "red",
        "tiles":
            [[[0, 0, 0],
              [1, 1, 0],
              [0, 1, 1]],

             [[0, 1, 0],
              [1, 1, 0],
              [1, 0, 0]]]
    },
    "O": {
        "color": "yellow",
        "tiles": [[[1, 1],
                   [1, 1]]]
    },
    "T": {
        "color": "magenta",
        "tiles":
            [[[0, 0, 0],
              [0, 1, 0],
              [1, 1, 1]],

             [[0, 1, 0],
              [1, 1, 0],
              [0, 1, 0]],

             [[0, 0, 0],
              [1, 1, 1],
              [0, 1, 0]],

             [[1, 0, 0],
              [1, 1, 0],
              [1, 0, 0]]]
    }
}

# Initialize the map variables
tile_size = 25
map_rows = 20
map_cols = 10
map_x = -125
map_y = 250

# Create the map turtle
map_turtle = turtle.Turtle()
map_turtle.hideturtle()
map_turtle.up()

# Create the game map using a list of lists
game_map = []
for row in range(map_rows):
    game_row = []
    for col in range(map_cols):
        game_row.append("")
    game_map.append(game_row)

# Initialize the block variables
active_block = None
active_block_row = 0
active_block_col = 0
active_block_index = 0

# Create the block turtle
block_turtle = turtle.Turtle()
block_turtle.hideturtle()
block_turtle.up()

# Initialize the game update interval
game_update_interval = 250

# Initialize the game score
score = 0

# Determine if the game is over or not
game_over = False


# This helper function draws a box with the given parameters using the turtle t
# The box is drawn from the top left hand corner
def draw_box(t, width, height, pencolor, fillcolor):
    t.color(pencolor, fillcolor)
    t.down()
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.right(90)
        t.forward(height)
        t.right(90)
    t.end_fill()
    t.up()


# This function draws the game map
def draw_map():
    map_turtle.clear()

    for row in range(map_rows):
        for col in range(map_cols):
            map_turtle.goto(map_x + tile_size * col, map_y - tile_size * row)

            # draw the tile for the current position
            if game_map[row][col] == "":
                draw_box(map_turtle, tile_size, tile_size, "black", "white")

            else:
                block_color = blocks[game_map[row][col]]["color"]

                draw_box(map_turtle, tile_size, tile_size, "black", block_color)


# This function makes a new block to start from the top
def make_new_block():
    global active_block
    global active_block_row, active_block_col
    global active_block_index

    block_types = list(blocks.keys())

    # Randomly pick a block type
    active_block = block_types[random.randint(0, len(block_types) - 1)]

    # Set a block location
    active_block_row = 0
    active_block_col = 4

    # Set the block index (the block arrangement)
    active_block_index = 0


# This function draws the active block
def draw_block():
    block_turtle.clear()

    # Find the x and y position of the block
    x = map_x + active_block_col * tile_size
    y = map_y - active_block_row * tile_size

    # Task: draw the active block at the location (x, y)
    block_color = blocks[active_block]["color"]
    block_tiles = blocks[active_block]["tiles"][active_block_index]

    for row in range(len(block_tiles)):
        for col in range(len(block_tiles[row])):
            if block_tiles[row][col] == 1:
                block_turtle.goto(x + col * tile_size, y - row * tile_size)  # - means go down
                draw_box(block_turtle, tile_size, tile_size, "black", block_color)


# This function tests whether the block is valid given its information
def is_valid_block(block_type, block_row, block_col, block_index):
    # Task: determine if the block is valid with the given information
    block_tiles = blocks[block_type]["tiles"][block_index]

    for row in range(len(block_tiles)):
        for col in range(len(block_tiles[row])):
            if block_tiles[row][col] == 1:
                # test the position of the tile against the size of the map
                tile_row = block_row + row
                tile_col = block_col + col
                if tile_row < 0 or tile_row >= map_rows or \
                        tile_col < 0 or tile_col >= map_cols:
                    return False

                # test the content of the game map so that the tile is not
                # hiding a color tile on the map
                if game_map[block_row + row][block_col + col] != "":
                    return False

    # The block is valid
    return True


# This function sets the active block onto the game map
def set_block_on_map():
    # get the tile arrangement
    block_tiles = blocks[active_block]["tiles"][active_block_index]

    # Set the active block on the map
    for row in range(len(block_tiles)):
        for col in range(len(block_tiles[row])):
            if block_tiles[row][col] == 1:
                map_row = row + active_block_row
                map_col = col + active_block_col
                game_map[map_row][map_col] = active_block


# This function removes the completed rows on the map
def remove_completed_rows():
    global game_map
    global t2

    # step 1:create a new map
    new_map = []

    # step 2:copy the incomplete rows to the new map
    for row in range(len(game_map)):
        game_row = game_map[row]

        # if the row is incomplete,add it to the new map
        if "" in game_row:
            new_map.append(game_row)
        else:
            global score
            score = score + 10
            print("score", score)

            # add
            global completeCount, game_update_interval
            completeCount += 1
            print("currentSpeed", game_update_interval)
            print("completeCount:",completeCount)
            if completeCount == 5:
                incr = game_update_interval * 0.1
                game_update_interval = int(game_update_interval - incr)
                print("changeSpeed", game_update_interval)
                completeCount = 0
    # add
    t2.clear()
    t2.write("score: {}".format(score), font=("微软雅黑", 18, "normal"))

    # step 3:insert empty rows to the new map
    for row in range(0, map_rows - len(new_map)):
        # add an empty row
        game_row = []
        for col in range(map_cols):
            game_row.append("")

        new_map.insert(0, game_row)

    # step 4:replace the original map with the new map
    game_map = new_map


# This function is the game loop which updates in fixed intervals
def game_loop():
    global active_block, active_block_row

    # change
    global stopFlag, t, game_over
    if not stopFlag:
        return

    # If there is no active block, make one
    if active_block == None:
        # make a new block here
        make_new_block()
        # if the new block is not valid,game is over
        if not is_valid_block(active_block, active_block_row, active_block_col, active_block_index):
            print("Game over!")
            game_over = True
            t.write("GAME OVER!", font=("微软雅黑", 28, "normal"))
            return

        # draw the block
        # print(active_block, active_block_row, active_block_col, active_block_index)
        draw_block()

    # Move the active block one row down
    else:
        # move the active block down
        new_block_row = active_block_row + 1

        # check if the block is valid
        if is_valid_block(active_block, new_block_row, active_block_col, active_block_index):
            active_block_row = new_block_row

            # update the block
            draw_block()

        else:
            # set the block on the map
            set_block_on_map()

            # find and remove completed rows
            remove_completed_rows()

            # update the map
            draw_map()

            # remove the block
            active_block = None

    turtle.update()

    # Set the next update

    turtle.ontimer(game_loop, game_update_interval)


# Set up the turtle window
turtle.setup(800, 600)
turtle.hideturtle()
turtle.tracer(False)
turtle.bgpic("hkust.gif")
turtle.up()

# add
t = turtle.Turtle()
t.hideturtle()
t._tracer(False)
t.goto(-120, -20)
t2 = turtle.Turtle()
t2._tracer(False)
t2.hideturtle()
t2.penup()
t2.goto(180, 220)
t2.pencolor("red")
t2.write("score: {}".format(score), font=("微软雅黑", 18, "normal"))

# Draw the background border around the map
turtle.goto(map_x - 10, map_y + 10)
draw_box(turtle, tile_size * map_cols + 20, tile_size * map_rows + 20, \
         "", "skyblue")
# Draw the empty map in the window
draw_map()
turtle.update()

# Set up the game loop
turtle.ontimer(game_loop, game_update_interval)


# This function handles the rotation of the block
def rotate():
    global active_block_index

    if active_block == None:
        return

    active_block_index = active_block_index + 1
    if active_block_index == len(blocks[active_block]["tiles"]):
        active_block_index = 0
    draw_block()


# This function handles the left movement of the block
def move_left():
    global active_block_col

    if active_block == None:
        return

    new_block_col = active_block_col - 1
    if is_valid_block(active_block, active_block_row, new_block_col, active_block_index):
        active_block_col = new_block_col

        draw_block()


# This function handles the right movement of the block
def move_right():
    global active_block_col

    # there is no active block
    if active_block == None:
        return

    new_block_col = active_block_col + 1
    # print(active_block, active_block_row, new_block_col, active_block_index)
    if is_valid_block(active_block, active_block_row, new_block_col, active_block_index):
        active_block_col = new_block_col

        draw_block()


# This function drop the block down the map
def drop():
    global active_block_row

    # print(active_block, new_block_row, active_block_row, active_block_index)

    # there is no active block
    if active_block == None:
        return

    # move the block down
    new_block_row = active_block_row + 1

    # move further until the block is invalid
    while is_valid_block(active_block, new_block_row, active_block_col, active_block_index):
        new_block_row = new_block_row + 1

    active_block_row = new_block_row - 1

    # update the block
    draw_block()


stopFlag = True


def stop():
    global stopFlag
    global t
    if not game_over:
        if stopFlag:
            stopFlag = False
        else:
            stopFlag = True
            turtle.ontimer(game_loop, game_update_interval)
            t.clear()


def changeBlock():
    global active_block_row, active_block_col, active_block
    if not active_block:
        return
    currentBlock = active_block
    currentRow, currentCol = active_block_row, active_block_col
    while True:
        make_new_block()
        if active_block != currentBlock:
            active_block_row = currentRow
            active_block_col = currentCol
            if is_valid_block(active_block, active_block_row, active_block_col, active_block_index):
                break
    draw_block()

# Set up the key handlers
turtle.onkeypress(rotate, "Up")
turtle.onkeypress(move_left, "Left")
turtle.onkeypress(move_right, "Right")
turtle.onkeypress(drop, "Down")

# add
currentDifficult = 0
completeCount = 0
turtle.onkeypress(stop, "space")
turtle.onkeypress(changeBlock, "c")

turtle.listen()
turtle.done()
