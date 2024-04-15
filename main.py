import pygame
import sys
import random

pygame.init()

# Värit
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Näytön koko
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Matopeli')

# Kellon alustus
clock = pygame.time.Clock()

# Muuttujia
snake_speed = 15
snake_size = 15
snake_pos = [[100, 50]]
snake_direction = 'DOWN'
snake_new_direction = 'DOWN'
food_pos = [random.randrange(1, (width//snake_size)) * snake_size, random.randrange(1, (height//snake_size)) * snake_size]
food_spawn = True
score = 0

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (width/10, 15)
    else:
        score_rect.midtop = (width/2, height/1.25)
    screen.blit(score_surface, score_rect)

# Pääsilmukka
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_direction != 'DOWN':
                snake_new_direction = 'UP'
            elif event.key == pygame.K_DOWN and snake_direction != 'UP':
                snake_new_direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake_direction != 'RIGHT':
                snake_new_direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake_direction != 'LEFT':
                snake_new_direction = 'RIGHT'
        elif event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Päivitä madon pään sijainti
    if snake_new_direction == 'UP':
        new_head = [snake_pos[0][0], snake_pos[0][1] - snake_size]
    elif snake_new_direction == 'DOWN':
        new_head = [snake_pos[0][0], snake_pos[0][1] + snake_size]
    elif snake_new_direction == 'LEFT':
        new_head = [snake_pos[0][0] - snake_size, snake_pos[0][1]]
    elif snake_new_direction == 'RIGHT':
        new_head = [snake_pos[0][0] + snake_size, snake_pos[0][1]]

    # Tarkista törmäys seinään ja resetoi peli tarvittaessa
    if new_head[0] >= width or new_head[0] < 0 or new_head[1] >= height or new_head[1] < 0:
        snake_pos = [[100, 50]]
        snake_direction = 'DOWN'
        snake_new_direction = 'DOWN'
        food_pos = [random.randrange(1, (width//snake_size)) * snake_size, random.randrange(1, (height//snake_size)) * snake_size]
        food_spawn = True
        score = 0
        continue

    # Lisää uusi pää madolle
    snake_pos.insert(0, new_head)
    snake_direction = snake_new_direction

    # Tarkista syöminen
    if snake_pos[0] == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_pos.pop()

    # Ruuan spawn
    if not food_spawn:
        food_pos = [random.randrange(1, (width//snake_size)) * snake_size, random.randrange(1, (height//snake_size)) * snake_size]
        food_spawn = True

    # Tarkista törmäys itseensä
    if snake_pos[0] in snake_pos[1:]:
        snake_pos = [[100, 50]]
        snake_direction = 'DOWN'
        snake_new_direction = 'DOWN'
        food_pos = [random.randrange(1, (width//snake_size)) * snake_size, random.randrange(1, (height//snake_size)) * snake_size]
        food_spawn = True
        score = 0
        continue

    # Piirtäminen
    screen.fill(BLACK)
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))
    show_score(1, WHITE, 'consolas', 20)
    pygame.display.update()

    # Päivitä kellon aika
    clock.tick(snake_speed)
