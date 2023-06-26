import pygame as pg
from random import randrange

pg.init()

clock = pg.time.Clock()

W = 420
H = 420
screen = pg.display.set_mode((W, H + 100))
pg.display.set_caption('Snake')

my_font = pg.font.SysFont(None, 30)

block_size = 20

block_img = pg.image.load('block.png')
block_img = pg.transform.scale(block_img, (block_size, block_size))

# define colors
colours = {'bg': "#3c2b2e", 'snake': "#eff1ed", 'score': "#f9e5d7"}


def draw_text(text, font, t_color, x_text, y_text):
    font_img = font.render(text, True, t_color)
    screen.blit(font_img, (x_text, y_text))


def read_from_file(file_name):
    some_file = open(file_name, "r")
    file_content = some_file.read()
    some_file.close()
    return file_content


def write_to_file(file_name, file_content):
    some_file = open(file_name, "w")
    some_file.write(file_content)
    some_file.close()


def shift_coord(some_list, some_length):
    for j in reversed(range(some_length - 1)):
        for i in range(2):
            some_list[j + 1][i] = some_list[j][i]


def increase_snake_n_moving_food(s_list, length, some_x, some_y):
    # increasing snake
    length += 1
    s_list.insert(0, [some_x, some_y])
    # moving food
    while True:
        some_x = randrange(0, W - block_size, block_size)
        some_y = randrange(0, H - block_size, block_size)
        if not [some_x, some_y] in s_list:
            break

    return s_list, length, some_x, some_y


def moving_through_the_field_size(some_coords):
    if some_coords[0] == W:
        some_coords[0] = 0
    elif some_coords[0] == -block_size:
        some_coords[0] = W
    elif some_coords[1] == -block_size:
        some_coords[1] = H - block_size
    elif some_coords[1] == H:
        some_coords[1] = 0
    return some_coords


x = None
y = None
is_moving = None
snake_speed = None
snake_length = None
food_x = None
food_y = None
snake_list = None
game_paused = None
pause_counter = None
game_over = None


def set_initial_parameters():
    global x, y, is_moving,snake_list, snake_speed, snake_length, food_x, food_y, game_over, game_paused, pause_counter
    x0 = 200
    y0 = 160
    x = x0
    y = y0
    # in is_moving axis 0 - x axis, axis 1 - y axis,
    # direction 1 - x or y coordinate increases, direction -1 - decreases,
    # direction 0 - coordinate doesn't change
    is_moving = {'axis': 0, 'direction': 0}
    snake_speed = block_size
    food_x = randrange(0, W - block_size, block_size)
    food_y = randrange(0, H - block_size, block_size)

    snake_list = []
    snake_length = 4
    for i in range(snake_length):
        snake_list.append([x0 - i * block_size, y0])

    game_paused = False
    pause_counter = 0
    game_over = False


set_initial_parameters()

run = True

while run:

    clock.tick(10)

    screen.fill(colours['bg'])

    # displaying score and level number
    if not game_over:
        pg.draw.rect(screen, colours['score'], pg.Rect(0, 420, W, 100))
        draw_text('Level 1', my_font, colours['bg'], 40, 440)
        draw_text('Pause: P', my_font, colours['bg'], 245, 440)
        draw_text('Your score =', my_font, colours['bg'], 40, 480)
        screen.blit(my_font.render(str(snake_length - 4), True, colours['bg']), (170, 480))
        h = read_from_file("hs.txt")
        draw_text('Highscore:', my_font, colours['bg'], 245, 480)
        screen.blit(my_font.render(h, True, colours['bg']), (355, 480))

    # initial moving of the snake
    if is_moving['direction'] == 0:
        if not game_paused:
            shift_coord(snake_list, snake_length)
            snake_list[0][0] += snake_speed
            # moving through the field sides
            snake_list[0] = moving_through_the_field_size(snake_list[0])
        if snake_list[0][0] == food_x and snake_list[0][1] == food_y:
            snake_list, snake_length, food_x, food_y = increase_snake_n_moving_food(snake_list, snake_length, food_x,
                                                                                    food_y)
        for i in range(snake_length):
            if snake_list[i][0] == W:
                snake_list[i][0] = 0
    # moving of the snake
    else:
        # coordinates of a head on the next step
        next_head_pos = [snake_list[0][0], snake_list[0][1]]
        next_head_pos[is_moving['axis']] += is_moving['direction'] * snake_speed
        # moving through the field sides
        next_head_pos = moving_through_the_field_size(next_head_pos)
        # if head eats food on the next step, block with the food coordinates is added to the head of the snake
        # and the food block is moved on it's next position
        if next_head_pos[0] == food_x and next_head_pos[1] == food_y:
            snake_list, snake_length, food_x, food_y = increase_snake_n_moving_food(snake_list, snake_length, food_x,
                                                                                    food_y)
        # change_coord shifts coordinates of length - 1 elements and next row changes coordinates of the head
        if not game_paused:
            shift_coord(snake_list, snake_length)
            snake_list[0][is_moving['axis']] += is_moving['direction'] * snake_speed

    # moving through the field sides
    snake_list[0] = moving_through_the_field_size(snake_list[0])

    # drawing the snake
    if not game_over:
        for i in range(snake_length):
            screen.blit(block_img, (snake_list[i][0], snake_list[i][1]))

    # drawing food
    if not game_over:
        pg.draw.rect(screen, colours['snake'], (food_x, food_y, block_size, block_size))

    # collision with itself
    for i in range(snake_length - 3):
        if snake_list[0][0] == snake_list[i + 3][0] and snake_list[0][1] == snake_list[i + 3][1]:
            snake_speed = 0
            game_over = True

    # displaying score at the end of a game
    if game_over:
        h = read_from_file("hs.txt")

        if snake_length - 4 >= int(h):
            write_to_file("hs.txt", str(snake_length - 4))

        h = read_from_file("hs.txt")
        draw_text('Highscore:', my_font, colours['score'], 140, 240)
        screen.blit(my_font.render(h, True, colours['score']), (270, 240))
        draw_text('Game Over', my_font, colours['score'], 160, 100)
        draw_text('Your score:', my_font, colours['score'], 140, 200)
        screen.blit(my_font.render(str(snake_length - 4), True, colours['score']), (270, 200))
        draw_text('Press R to restart', my_font, colours['snake'], 130, 380)

    motion_keys = {
        pg.K_DOWN: (1, 1),
        pg.K_UP: (1, -1),
        pg.K_RIGHT: (0, 1),
        pg.K_LEFT: (0, -1)
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        # defining keys
        if event.type == pg.KEYDOWN:
            if event.key in motion_keys:
                if is_moving['axis'] != motion_keys[event.key][0]:  # snake can't go backwards
                    is_moving['axis'] = motion_keys[event.key][0]
                    is_moving['direction'] = motion_keys[event.key][1]
            # restart the game
            if event.key == pg.K_r and game_over:
                set_initial_parameters()
            if event.key == pg.K_p:
                pause_counter += 1
                if pause_counter % 2 == 0:
                    game_paused = False
                else:
                    game_paused = True

    pg.display.flip()






