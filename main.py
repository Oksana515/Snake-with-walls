import pygame as pg
from random import randrange

pg.init()

clock = pg.time.Clock()

W = 420
H = 420
screen = pg.display.set_mode((W, H))
pg.display.set_caption('Snake')

my_font = pg.font.SysFont(None, 30)

block_size = 20

block_img = pg.image.load('block.png')
block_img = pg.transform.scale(block_img, (block_size, block_size))


def draw_text(text, font, t_color, x_text, y_text):
    font_img = font.render(text, True, t_color)
    screen.blit(font_img, (x_text, y_text))


chocolate_color = "#815854"
cream_color = "#F9EBDE"
BG = chocolate_color


def shift_coord(some_list, some_length):
    for j in reversed(range(some_length - 1)):
        for i in range(2):
            some_list[j + 1][i] = some_list[j][i]


def add_block(s_list, length):
    side_indicator = []
    x1 = s_list[length - 1][0]
    x2 = s_list[length - 2][0]
    y1 = s_list[length - 1][1]
    y2 = s_list[length - 2][1]

    if y1 == y2 and (x2 - x1 == block_size or x2 - x1 == W):
        side_indicator = [-1, 0]
    elif y1 == y2 and (x1 - x2 == block_size or x1 - x2 == W):
        side_indicator = [1, 0]
    elif x1 == x2 and (y2 - y1 == block_size or y2 - y1 == H):
        side_indicator = [0, -1]
    elif x1 == x2 and (y1 - y2 == block_size or y1 - y2 == H):
        side_indicator = [0, 1]

    print(x1, y1, x2, y2)

    s_list.append([s_list[length - 1][0] + side_indicator[0] * block_size,
                   s_list[length - 1][1] + side_indicator[1] * block_size])

    length += 1
    return s_list, length


x = None
y = None
is_moving = None
snake_speed = None
snake_length = None
food_x = None
food_y = None
snake_list = None
food_eaten = None
game_over = None


def set_initial_parameters():
    global x, y, is_moving,snake_list, snake_speed, snake_length, food_x, food_y, food_eaten, game_over
    x0 = 200
    y0 = 160
    x = x0
    y = y0
    # in is_moving axis 0 - x axis, axis 1 - y axis,
    # direction 1 - x or y coordinate increases, direction -1 - decreases,
    # direction 0 - coordinate doesn't change
    is_moving = {'axis': 0, 'direction': 0}
    snake_speed = block_size
    food_x = 400
    food_y = 240

    snake_list = []
    snake_length = 4
    for i in range(snake_length):
        snake_list.append([x0 - i * block_size, y0])

    food_eaten = False
    game_over = False


set_initial_parameters()

run = True

while run:

    clock.tick(10)

    screen.fill(BG)

    # drawing food
    if not game_over:
        pg.draw.rect(screen, cream_color, (food_x, food_y, block_size, block_size))

    # displaying score at the end of a game
    if game_over:
        draw_text('Game Over', my_font, cream_color, 160, 130)
        draw_text('Your score =', my_font, cream_color, 140, 180)
        screen.blit(my_font.render(str(snake_length - 4), True, cream_color), (270, 180))
        draw_text('Press R to restart', my_font, cream_color, 130, 250)

    # eating food and removing next food to another place
    if snake_list[0][0] == food_x and snake_list[0][1] == food_y:
        food_eaten = True
        food_x = randrange(0, W - block_size, block_size)
        food_y = randrange(0, H - block_size, block_size)

    # collision with itself
    for i in range(snake_length - 3):
        if snake_list[0][0] == snake_list[i+3][0] and snake_list[0][1] == snake_list[i+3][1]:
            snake_speed = 0
            game_over = True

    # initial moving of the snake
    if is_moving['direction'] == 0:
        for i in range(snake_length):
            snake_list[i][0] += snake_speed
            if snake_list[i][0] == W:
                snake_list[i][0] = 0
    # moving of the snake
    else:
        # change_coord shifts coordinates of length - 1 elements and next row changes coordinates of the head
        shift_coord(snake_list, snake_length)
        snake_list[0][is_moving['axis']] += is_moving['direction'] * snake_speed
        if food_eaten:
            snake_list, snake_length = add_block(snake_list, snake_length)
            food_eaten = False

    # moving through the field sides
    if snake_list[0][0] == W:
        snake_list[0][0] = 0
    elif snake_list[0][0] == -block_size:
        snake_list[0][0] = W
    elif snake_list[0][1] == -block_size:
        snake_list[0][1] = H
    elif snake_list[0][1] == H:
        snake_list[0][1] = 0

    # drawing the snake
    if not game_over:
        for i in range(snake_length):
            screen.blit(block_img, (snake_list[i][0], snake_list[i][1]))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # defining keys
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN:
                is_moving['axis'] = 1
                is_moving['direction'] = 1
            if event.key == pg.K_UP:
                is_moving['axis'] = 1
                is_moving['direction'] = -1
            if event.key == pg.K_RIGHT:
                is_moving['axis'] = 0
                is_moving['direction'] = 1
            if event.key == pg.K_LEFT:
                is_moving['axis'] = 0
                is_moving['direction'] = -1
            # restart the game
            if event.key == pg.K_r and game_over:
                set_initial_parameters()

    pg.display.flip()




