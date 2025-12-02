import pygame
import random
import time
import os
pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (150, 150, 150)
GOLD = (255, 215, 0)
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
HIGHSCORE_FILE = 'highscore.txt'

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game by Arun - bored dev? press w to start')

clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 35)
score_font = pygame.font.SysFont("comicsans", 25)
#he he 

def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        try:
            with open(HIGHSCORE_FILE, 'r') as f:
                return int(f.read().strip())
        except:
            return 0
    return 0
# :C
def save_highscore(score):
    with open(HIGHSCORE_FILE, 'w') as f:
        f.write(str(score))

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

def game_loop():
    game_over = False
    game_close = False
    paused = False
    pause_button = pygame.Rect(470, 10, 110, 35)
    highscore = load_highscore()
    x = WIDTH // 2
    y = HEIGHT // 2

    x_change = 0
    y_change = 0
    snake = []
    length = 1
    food_x = round(random.randrange(0, WIDTH - GRID_SIZE) / GRID_SIZE) * GRID_SIZE
    food_y = round(random.randrange(0, HEIGHT - GRID_SIZE) / GRID_SIZE) * GRID_SIZE
    score = 0
    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message = font.render("You Lost!", True, RED)
            screen.blit(message, [WIDTH//2 - message.get_width()//2, HEIGHT//3])
            
            score_text = score_font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, [WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20])

            highscore_text = score_font.render(f"High Score: {highscore}", True, GOLD)
            screen.blit(highscore_text, [WIDTH//2 - highscore_text.get_width()//2, HEIGHT//2 + 20])

            restart_text = score_font.render("Press Q-Quit or C-Play Again", True, WHITE)
            screen.blit(restart_text, [WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 70])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

            continue 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -GRID_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = GRID_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -GRID_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = GRID_SIZE
                    x_change = 0
                elif event.key == pygame.K_a and x_change == 0:
                    x_change = -GRID_SIZE
                    y_change = 0
                elif event.key == pygame.K_d and x_change == 0:
                    x_change = GRID_SIZE
                    y_change = 0
                elif event.key == pygame.K_w and y_change == 0:
                    y_change = -GRID_SIZE
                    x_change = 0
                elif event.key == pygame.K_s and y_change == 0:
                    y_change = GRID_SIZE
                    x_change = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.collidepoint(event.pos):
                    paused = not paused
        if not paused:
            x += x_change
            y += y_change
            snake_head = [x, y]
            snake.append(snake_head)
            if len(snake) > length:
                del snake[0]
            if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
                game_close = True
            for segment in snake[:-1]:
                if segment == snake_head:
                    game_close = True
            if x == food_x and y == food_y:
                food_x = round(random.randrange(0, WIDTH - GRID_SIZE) / GRID_SIZE) * GRID_SIZE
                food_y = round(random.randrange(0, HEIGHT - GRID_SIZE) / GRID_SIZE) * GRID_SIZE
                length += 1
                score += 1
                if score > highscore:
                    highscore = score
                    save_highscore(highscore)
        screen.fill(BLACK)
        draw_grid()
        pygame.draw.rect(screen, GREEN, [food_x, food_y, GRID_SIZE, GRID_SIZE])
        for segment in snake:
            pygame.draw.rect(screen, BLUE, [segment[0], segment[1], GRID_SIZE, GRID_SIZE])
            pygame.draw.rect(screen, WHITE, [segment[0]+4, segment[1]+4, 12, 12]) 
        score_text = score_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, [10, 10])
        
        highscore_text = score_font.render(f"High: {highscore}", True, GOLD)
        screen.blit(highscore_text, [10, 40])
        mouse_pos = pygame.mouse.get_pos()
        hovered = pause_button.collidepoint(mouse_pos)
        button_color = LIGHT_GRAY if hovered else GRAY
        pygame.draw.rect(screen, button_color, pause_button)
        pygame.draw.rect(screen, WHITE, pause_button, 3 if hovered else 2)
        button_text = score_font.render("PAUSE" if not paused else "RESUME", True, BLACK)
        text_rect = button_text.get_rect(center=pause_button.center)
        screen.blit(button_text, text_rect)
        if paused:
            paused_text = font.render("PAUSED", True, RED)
            paused_rect = paused_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(paused_text, paused_rect)

        pygame.display.update()
        clock.tick(12 if not paused else 60)
 #alr bruh 

    pygame.quit()
    quit()
game_loop()
