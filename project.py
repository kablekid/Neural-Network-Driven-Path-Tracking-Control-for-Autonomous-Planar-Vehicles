import pygame, sys

pygame.init()


info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("Simple Circle Movement with Wall Collision")


BLUE = (0, 120, 255)
RED = (255, 0, 0)

radius = 25
x, y = WIDTH // 2, HEIGHT // 2
speed = 5

walls = [
    pygame.Rect(0, 0, WIDTH, 20),           # top
    pygame.Rect(0, HEIGHT - 20, WIDTH, 20), # bottom
    pygame.Rect(0, 0, 20, HEIGHT),          # left
    pygame.Rect(WIDTH - 20, 0, 20, HEIGHT)  # right
]

clock = pygame.time.Clock()

while True:
    dt = clock.tick(60) / 1000  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    dx = dy = 0
    if keys[pygame.K_UP]:
        dy = -speed
    if keys[pygame.K_DOWN]:
        dy = speed
    if keys[pygame.K_LEFT]:
        dx = -speed
    if keys[pygame.K_RIGHT]:
        dx = speed


    next_rect = pygame.Rect(x + dx - radius, y + dy - radius, radius * 2, radius * 2)
    collision = False

    for wall in walls:
        if next_rect.colliderect(wall):
            collision = True
            break

    
    if not collision:
        x += dx
        y += dy

    screen.fill((30, 30, 30))

    pygame.draw.circle(screen, BLUE, (int(x), int(y)), radius)

    for wall in walls:
        pygame.draw.rect(screen, RED, wall)

    pygame.display.flip()
