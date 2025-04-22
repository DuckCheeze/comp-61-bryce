import pygame 
import sys
import random
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Burger Flip Frenzy")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLATE_COLOR = (200, 200, 200)
TIMER_COLOR = (0, 255, 0)
RED = (255, 0, 0)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

# Burger properties
burger_radius = 60
burger_x = WIDTH // 2
burger_y = HEIGHT // 2
burger_dx = 5
burger_dy = -10
burger_gravity = 0.5
burger_on_plate = False
burger_rotation = 0

# Load burger image
burger_img = pygame.image.load("burger.png")
burger_img = pygame.transform.scale(burger_img, (burger_radius * 2, burger_radius * 2))

# Plate properties
plate_width = 200
plate_height = 20
plate_x = WIDTH // 2 - plate_width // 2
plate_y = HEIGHT - 60
plate_speed = 20

# Timer properties
timer_count = 3
last_timer_tick = pygame.time.get_ticks()

# Score
score = 0
high_score = 0

# Game state
game_active = False

# Play background grill sound
pygame.mixer.music.load("grill_background.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# Load corgi image and set size
corgi_img = pygame.image.load("corgispat.png")
corgi_rect = corgi_img.get_rect()
corgi_x = random.randint(0, WIDTH - corgi_rect.width)
corgi_y = random.randint(0, HEIGHT - corgi_rect.height)
corgi_dx = random.choice([-2, 2])
corgi_dy = random.choice([-2, 2])

# Corgi floating message setup
corgi_messages = [
    "Woof!", "Flip that burger!", "You're on Fire!", "You got this!", "Nice catch!",
    "Yurrrrrrrrrr", "You're a baller!", "Nice flip, rookie!", "I love you in that outfit",
    "Keep up them flips!", "Better than McDonalds", "Not an idiot sandwich", "Nobody outflips Chef Corgi!"
]
current_corgi_message = random.choice(corgi_messages)
last_message_change = pygame.time.get_ticks()
message_change_interval = 5000  # milliseconds

# Load background images
background_img = pygame.image.load("backdropburger.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

corgikitchen_img = pygame.image.load("corgikitchen.png")
corgikitchen_img = pygame.transform.scale(corgikitchen_img, (WIDTH, HEIGHT))

def draw_home_screen():
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))  # Home screen background

    title = font.render("Burger Flip Frenzy", True, WHITE)
    instruction = small_font.render("Press SPACE to Start", True, WHITE)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 40))
    screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 100))

    pygame.display.flip()

def draw_rules_screen():
    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))  # Rules screen background

    rules_title = font.render("How to Play", True, WHITE)
    rules_text = [
        "Use the LEFT and RIGHT arrow keys to move the plate.",
        "Catch the falling burger and flip it back up!",
        "Don't let it hit the floor or run out of time!",
        "WARNING: Chef Corgi is adorable and distracting.",
        "",
        "RANKS:",
        "10 flips: Rookie",
        "20 flips: Burger Flipper",
        "50 flips: Real Chef",
        "100 flips: Michelin Star",
        "200 flips: Head Chef"
    ]

    screen.blit(rules_title, (WIDTH // 2 - rules_title.get_width() // 2, 40))
    for i, line in enumerate(rules_text):
        text = small_font.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 120 + i * 30))

    press_space = small_font.render("Press ENTER to Start", True, WHITE)
    screen.blit(press_space, (WIDTH // 2 - press_space.get_width() // 2, HEIGHT - 100))

    pygame.display.flip()

def draw_game_elements():
    screen.fill(BLACK)
    screen.blit(corgikitchen_img, (0, 0))  # Game background

    rotated_burger = pygame.transform.rotate(burger_img, burger_rotation)
    burger_rect = rotated_burger.get_rect(center=(int(burger_x), int(burger_y)))
    screen.blit(rotated_burger, burger_rect)

    pygame.draw.rect(screen, PLATE_COLOR, (plate_x, plate_y, plate_width, plate_height))

    time_width = max(0, int((timer_count / 3) * WIDTH))
    pygame.draw.rect(screen, TIMER_COLOR if timer_count > 1 else RED, (0, 0, time_width, 10))

    score_text = small_font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 20))
    high_score_text = small_font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 20))

    screen.blit(corgi_img, (corgi_x, corgi_y))
    corgi_message_text = small_font.render(current_corgi_message, True, WHITE)
    screen.blit(corgi_message_text, (corgi_x + corgi_img.get_width() // 2 + 10, corgi_y))

    pygame.display.flip()

def draw_game_over():
    global high_score
    screen.fill(BLACK)
    screen.blit(corgikitchen_img, (0, 0))  # Game over background

    over_text = font.render("Game Over!", True, WHITE)
    score_text = small_font.render(f"Final Score: {score}", True, WHITE)
    restart_text = small_font.render("Press SPACE to Restart", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 40))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

def reset_game():
    global burger_x, burger_y, burger_dx, burger_dy, burger_on_plate, timer_count, score, burger_rotation
    burger_x = WIDTH // 2
    burger_y = HEIGHT // 2
    burger_dx = random.choice([-5, 5])
    burger_dy = -10
    burger_on_plate = False
    timer_count = 3
    score = 0
    burger_rotation = 0

def update_burger():
    global burger_x, burger_y, burger_dx, burger_dy, burger_on_plate, burger_rotation

    if not burger_on_plate:
        burger_x += burger_dx
        burger_y += burger_dy
        burger_dy += burger_gravity
        burger_rotation += 5 if burger_dx > 0 else -5

        if burger_x - burger_radius <= 0 or burger_x + burger_radius >= WIDTH:
            burger_dx *= -1

        if burger_y + burger_radius >= HEIGHT:
            burger_on_plate = True

def check_plate_collision():
    global burger_dy, burger_on_plate, timer_count, score
    if plate_y < burger_y + burger_radius < plate_y + plate_height:
        if plate_x < burger_x < plate_x + plate_width:
            burger_dy = -25
            burger_on_plate = False
            timer_count = 3
            score += 1

def update_corgi():
    global corgi_x, corgi_y, corgi_dx, corgi_dy
    corgi_x += corgi_dx
    corgi_y += corgi_dy

    if corgi_x <= 0 or corgi_x + corgi_img.get_width() >= WIDTH:
        corgi_dx *= -1
    if corgi_y <= 0 or corgi_y + corgi_img.get_height() >= HEIGHT:
        corgi_dy *= -1

def game_loop():
    global plate_x, timer_count, last_timer_tick, game_active, high_score, current_corgi_message, last_message_change, show_rules_screen, game_started

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if not game_started:
            if show_rules_screen:
                draw_rules_screen()
                if keys[pygame.K_RETURN]:
                    show_rules_screen = False
                    reset_game()
                    game_started = True
                    time.sleep(0.2)
            else:
                draw_home_screen()
                if keys[pygame.K_SPACE]:
                    show_rules_screen = True
                    time.sleep(0.2)
            continue

        if game_active:
            if keys[pygame.K_LEFT] and plate_x > 0:
                plate_x -= plate_speed
            if keys[pygame.K_RIGHT] and plate_x + plate_width < WIDTH:
                plate_x += plate_speed

            update_burger()
            check_plate_collision()
            update_corgi()

            now = pygame.time.get_ticks()
            if now - last_message_change > message_change_interval:
                new_message = random.choice([msg for msg in corgi_messages if msg != current_corgi_message])
                current_corgi_message = new_message
                last_message_change = now

            if now - last_timer_tick >= 1000:
                timer_count -= 1
                last_timer_tick = now

            draw_game_elements()

            if burger_on_plate and burger_y + burger_radius >= HEIGHT:
                if score > high_score:
                    high_score = score
                draw_game_over()
                game_active = False
                time.sleep(1)

            if timer_count <= 0:
                if score > high_score:
                    high_score = score
                draw_game_over()
                game_active = False
                time.sleep(1)

        if not game_active and keys[pygame.K_SPACE]:
            game_active = True
            reset_game()
            time.sleep(0.2)

        clock.tick(60)

# Game state flags
show_rules_screen = False
game_started = False
game_active = True

game_loop()