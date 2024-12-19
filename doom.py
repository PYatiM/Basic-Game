import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Doom-Inspired Shooting Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Clock
clock = pygame.time.Clock()

# Assets
background_img = pygame.image.load("background.jpg")
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")
bullet_img = pygame.image.load("bullet.png")
powerup_img = pygame.image.load("powerup.png")
boss_img = pygame.image.load("boss.png")

# Sounds
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
powerup_sound = pygame.mixer.Sound("powerup.wav")
hit_boss_sound = pygame.mixer.Sound("boss_hit.wav")
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)  # Loop background music

# Player settings
player = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 75, 50, 50)
PLAYER_SPEED = 5
health = 100

# Bullet settings
BULLET_SPEED = 10
bullets = []

# Enemy settings
ENEMY_SPEED = 3
enemies = []
spawn_rate = 50

# Power-up settings
POWERUP_SPAWN_RATE = 200
POWERUP_DURATION = 300  # Frames
powerups = []
powerup_active = False
powerup_timer = 0

# Boss settings
boss_active = False
boss = pygame.Rect(SCREEN_WIDTH // 2 - 50, -100, 100, 100)
boss_health = 50

# Scoring and levels
score = 0
level = 1
font = pygame.font.Font(None, 36)

# Game state
game_over = False


def spawn_enemy():
    if random.randint(1, spawn_rate) == 1:
        size = random.choice([50, 70])
        speed = random.choice([ENEMY_SPEED, ENEMY_SPEED + 1])
        enemy = pygame.Rect(random.randint(0, SCREEN_WIDTH - size), 0, size, size)
        enemies.append({"rect": enemy, "speed": speed})


def spawn_powerup():
    if random.randint(1, POWERUP_SPAWN_RATE) == 1:
        powerup = pygame.Rect(random.randint(0, SCREEN_WIDTH - 30), 0, 30, 30)
        powerups.append(powerup)


def move_bullets():
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.y < 0:
            bullets.remove(bullet)


def move_enemies():
    global health, game_over
    for enemy in enemies[:]:
        enemy["rect"].y += enemy["speed"]
        if enemy["rect"].colliderect(player):
            health -= 20
            enemies.remove(enemy)
            if health <= 0:
                game_over = True
        elif enemy["rect"].y > SCREEN_HEIGHT:
            enemies.remove(enemy)


def move_powerups():
    global powerup_active, powerup_timer
    for powerup in powerups[:]:
        powerup.y += 2
        if powerup.colliderect(player):
            powerup_active = True
            powerup_timer = POWERUP_DURATION
            powerup_sound.play()
            powerups.remove(powerup)
        elif powerup.y > SCREEN_HEIGHT:
            powerups.remove(powerup)


def move_boss():
    global boss_active
    if boss_active:
        boss.y += 2
        if boss.y > SCREEN_HEIGHT:
            boss_active = False


def check_collisions():
    global score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy["rect"]):
                hit_sound.play()
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10
                break


def check_boss_collisions():
    global boss_active, boss_health, score
    for bullet in bullets[:]:
        if bullet.colliderect(boss):
            bullets.remove(bullet)
            boss_health -= 1
            hit_boss_sound.play()
            if boss_health <= 0:
                boss_active = False
                score += 50


def level_up():
    global level, ENEMY_SPEED, spawn_rate
    level += 1
    ENEMY_SPEED += 1
    spawn_rate = max(20, spawn_rate - 5)


def spawn_boss():
    global boss_active, boss_health
    boss_active = True
    boss_health = 50
    boss.x = SCREEN_WIDTH // 2 - 50
    boss.y = -100  # Start position off-screen


def draw_objects():
    screen.blit(background_img, (0, 0))
    screen.blit(player_img, player.topleft)
    for bullet in bullets:
        screen.blit(bullet_img, bullet.topleft)
    for enemy in enemies:
        screen.blit(enemy_img, enemy["rect"].topleft)
    for powerup in powerups:
        screen.blit(powerup_img, powerup.topleft)
    if boss_active:
        screen.blit(boss_img, boss.topleft)

    pygame.draw.rect(screen, RED, (10, 10, 200, 20))
    pygame.draw.rect(screen, GREEN, (10, 10, 2 * health, 20))

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 150, 40))


def reset_game():
    global bullets, enemies, powerups, score, health, game_over, powerup_active, powerup_timer, level, boss_active
    bullets = []
    enemies = []
    powerups = []
    score = 0
    health = 100
    game_over = False
    powerup_active = False
    powerup_timer = 0
    level = 1
    boss_active = False
    player.x = SCREEN_WIDTH // 2 - 25


def show_menu():
    screen.fill(BLACK)
    title = font.render("DOOM-Inspired Shooting Game", True, WHITE)
    play_button = font.render("Press ENTER to Play", True, GREEN)
    quit_button = font.render("Press Q to Quit", True, RED)
    screen.blit(title, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100))
    screen.blit(play_button, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
    screen.blit(quit_button, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


# Main Game Loop
show_menu()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - 5, player.y - 20, 10, 20)
                bullets.append(bullet)
                shoot_sound.play()
        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player.x < SCREEN_WIDTH - player.width:
            player.x += PLAYER_SPEED

        move_bullets()
        spawn_enemy()
        spawn_powerup()
        move_enemies()
        move_powerups()
        move_boss()
        check_collisions()
        check_boss_collisions()

        if powerup_active:
            BULLET_SPEED = 15
            powerup_timer -= 1
            if powerup_timer <= 0:
                powerup_active = False
                BULLET_SPEED = 10

        if score % 100 == 0 and score > 0 and not boss_active:
            spawn_boss()

    draw_objects()

    if game_over:
        game_over_text = font.render("Game Over! Press R to Restart", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
