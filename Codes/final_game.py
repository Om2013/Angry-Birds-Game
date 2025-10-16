confirm = input("Would you like to start the game? Y/N: ")

if confirm.upper() == "Y":
    print("Starting the game!")
else:
    exit()

import pygame
import pymunk
import pymunk.pygame_util

# Initialize Pygame
pygame.init()
screen_size = 800, 600
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Angry Bird Design")
clock = pygame.time.Clock()
FPS = 60

# Game variables
score = 0
attempts = 3
gameover = False
font = pygame.font.Font(None, 48)
bird_in_flight = False

# Pymunk space setup
space = pymunk.Space()
space.gravity = (0, 900)
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Load and resize images
background_image = pygame.image.load("angry_birds_background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, screen_size)

bird_image = pygame.image.load("angry_bird_image.png").convert_alpha()
bird_image = pygame.transform.scale(bird_image, (40, 40))

brick_image = pygame.image.load("brick_image.png").convert_alpha()
brick_image = pygame.transform.scale(brick_image, (60, 60))

pig_image = pygame.image.load("pig_image.png").convert_alpha()
pig_image = pygame.transform.scale(pig_image, (40, 40))

# Sounds
victory_sound = pygame.mixer.Sound("victory_sound_angry_birds.mp3")
lose_sound = pygame.mixer.Sound("lose_sound_angry_birds.mp3")
launch_sound = pygame.mixer.Sound("launch_sound_angry_birds.mp3")
hit_sound = pygame.mixer.Sound("hit_sound_angry_birds.mp3")
background_music = pygame.mixer.Sound("background_music_angry_birds.mp3")
background_music.play(-1)

# Ground
ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
ground_shape = pymunk.Segment(ground_body, (0, 580), (800, 580), 5)
ground_shape.friction = 1.0
ground_shape.elasticity = 0.8
space.add(ground_body, ground_shape)

# Bird
def create_bird(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.8
    shape.friction = 0.5
    space.add(body, shape)
    return body, shape

bird_body, bird_shape = create_bird(150, 500)

# Blocks
def create_block(x, y):
    body = pymunk.Body(1, pymunk.moment_for_box(1, (60, 60)))
    body.position = (x, y)
    shape = pymunk.Poly.create_box(body, (60, 60))
    shape.elasticity = 0.4
    shape.friction = 0.6
    space.add(body, shape)
    return body, shape

blocks = [
    create_block(600, 520), create_block(660, 520),
    create_block(720, 520), create_block(660, 480),
    create_block(690, 480), create_block(680, 440)
]

# Pigs
def create_pigs(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 20))
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.elasticity = 0.4
    shape.friction = 0.6
    space.add(body, shape)
    return body, shape

pigs = [create_pigs(650, 520), create_pigs(710, 520), create_pigs(670, 480)]

# Draw everything
def draw_objects():
    screen.blit(background_image, (0, 0))
    bird_pos = bird_body.position
    screen.blit(bird_image, (bird_pos.x - 20, bird_pos.y - 20))

    pygame.draw.line(screen, (0, 0, 0), (0, 580), (800, 580), 5)

    for body, shape in blocks:
        block_pos = body.position
        angle = body.angle
        rotated_brick = pygame.transform.rotate(brick_image, angle * (180 / 3.14159))
        rect = rotated_brick.get_rect(center=(block_pos.x, block_pos.y))
        screen.blit(rotated_brick, rect)

    for body, shape in pigs:
        pig_pos = body.position
        screen.blit(pig_image, (pig_pos.x - 20, pig_pos.y - 20))

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    attempts_text = font.render(f"Attempts: {attempts}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(attempts_text, (10, 50))

# Collision check
def check_collisions():
    global score
    for (pig_body, pig_shape) in pigs[:]:
        distance = (bird_body.position - pig_body.position).length
        if distance < 40:  # Hit
            hit_sound.play()
            space.remove(pig_body, pig_shape)
            pigs.remove((pig_body, pig_shape))
            score += 10

# Reset the bird
def reset_bird():
    global bird_body, bird_shape, bird_in_flight
    space.remove(bird_body, bird_shape)
    bird_body, bird_shape = create_bird(150, 500)
    bird_in_flight = False

# Main loop
running = True
while running:
    if gameover:
        screen.fill((255, 255, 255))
        msg = font.render("Game Over! Press R to Restart or Q to Quit", True, (255, 0, 0))
        screen.blit(msg, (80, 250))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    score = 0
                    attempts = 3
                    pigs = [create_pigs(650, 520), create_pigs(710, 520), create_pigs(670, 480)]
                    reset_bird()
                    gameover = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not bird_in_flight and attempts > 0:
            mouse_pos = pygame.mouse.get_pos()
            launch_sound.play()
            bird_body.position = 150, 500
            bird_body.velocity = ((mouse_pos[0] - 150) * 4, (500 - mouse_pos[1]) * 4)
            attempts -= 1
            bird_in_flight = True

    space.step(1 / FPS)
    draw_objects()
    check_collisions()

    # Bird reappears if it goes off screen or stops moving
    if bird_in_flight:
        vx, vy = bird_body.velocity
        if abs(vx) < 10 and abs(vy) < 10 or bird_body.position.y > 600 or bird_body.position.x > 820:
            reset_bird()

    # Win/Loss check
    if not pigs:
        background_music.stop()
        victory_sound.play()
        win_msg = font.render("You Win!", True, (0, 150, 0))
        screen.blit(win_msg, (330, 250))
        pygame.display.flip()
        pygame.time.delay(3000)
        gameover = True

    if attempts <= 0 and pigs and not bird_in_flight:
        background_music.stop()
        lose_sound.play()
        lose_msg = font.render("Out of Attempts!", True, (255, 0, 0))
        screen.blit(lose_msg, (270, 250))
        pygame.display.flip()
        pygame.time.delay(3000)
        gameover = True

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
