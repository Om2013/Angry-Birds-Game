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

# Pymunk space setup
space = pymunk.Space()
space.gravity = (0, 900)

# Load and resize images
bird_image = pygame.image.load("angry_bird_image.png").convert_alpha()
background_image = pygame.image.load("angry_birds_background.jpg").convert_alpha()
background_image = pygame.transform.scale(background_image, screen_size)

bird_image_new_size = (40, 40)
bird_image = pygame.transform.scale(bird_image, bird_image_new_size)

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

# Draw everything
def draw_objects():
    screen.blit(background_image, (0, 0))
    bird_pos = bird_body.position
    screen.blit(bird_image, (bird_pos.x - 20, bird_pos.y - 20))
    pygame.draw.line(screen, (0, 0, 0), (0, 580), (800, 580), 5)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            bird_body.position = (150, 500)
            bird_body.velocity = (mouse_pos[0] - 150) * 4,(500 - mouse_pos[1]) * 4  
    draw_objects()
    space.step(1 / FPS)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
