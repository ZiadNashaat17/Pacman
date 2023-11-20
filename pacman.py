from board import boards
import pygame
import math

pygame.init()

WIDTH = 800
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 20)
level = boards
color = 'blue'
PI = math.pi
player_images = []

for i in range(1, 5):
    image_path = f'assets/player_images/{i}.png'
    image = pygame.image.load(image_path)
    scaled_image = pygame.transform.scale(image, (30, 30))
    player_images.append(scaled_image)

player_x = 380
player_y = 476
direction = 0
counter = 0
flicker = False
turns_allowed = [False, False, False, False]


def draw_board():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1),), 2)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 8)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1),
                                 (j * num2 + (0.5 * num2), i * num1 + num1), 2)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 2)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1],
                                0, PI / 2, 2)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1],
                                PI / 2, PI, 2)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI,
                                3 * PI / 2, 2)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)), (i * num1 - (num1 * 0.4)), num2, num1],
                                3 * PI / 2, 2 * PI, 2)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2, i * num1 + (0.5 * num1)), 2)


def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    if direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    if direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    if direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


def check_position(centerX, centerY):
    turns = [False, False, False, False]
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    num3 = 15
    # check collisions based on center x and center y of player +/- fudge number
    if centerX // 30 < 29:
        if direction == 0:
            if level[centerY // num1][(centerX - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centerY // num1][(centerX + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centerY + num3) // num1][centerX // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centerY - num3) // num1][centerX // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 10 <= centerX % num2 <= 16:
                if level[(centerY + num3) // num1][centerX // num2] < 3:
                    turns[3] = True
                if level[(centerY - num3) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 10 <= centerX % num1 <= 16:
                if level[centerY // num1][(centerX - num2) // num2] < 3:
                    turns[1] = True
                if level[centerY // num1][(centerX + num2) // num2] < 3:
                    turns[0] = True

        if direction == 0 or direction == 1:
            if 10 <= centerX % num2 <= 16:
                if level[(centerY + num1) // num1][centerX // num2] < 3:
                    turns[3] = True
                if level[(centerY - num1) // num1][centerX // num2] < 3:
                    turns[2] = True
            if 10 <= centerX % num1 <= 16:
                if level[centerY // num1][(centerX - num3) // num2] < 3:
                    turns[1] = True
                if level[centerY // num1][(centerX + num3) // num2] < 3:
                    turns[0] = True

    else:
        turns[0] = True
        turns[1] = True

    return turns


run = True
while run:
    timer.tick(fps)
    if counter < 19:
        counter += 1
        if counter > 10:
            flicker = False
    else:
        counter = 0
        flicker = True
    screen.fill('black')
    draw_board()
    draw_player()
    center_x = player_x + 15
    center_Y = player_y + 16

    turns_allowed = check_position(center_x, center_Y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                direction = 0
            if event.key == pygame.K_LEFT:
                direction = 1
            if event.key == pygame.K_UP:
                direction = 2
            if event.key == pygame.K_DOWN:
                direction = 3
    pygame.display.flip()
pygame.quit()
