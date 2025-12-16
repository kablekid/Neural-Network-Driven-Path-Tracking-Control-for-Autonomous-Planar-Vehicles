import random
import pygame
import math
import DrivingEnv

pygame.init()

WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Driving Env with Rays")
background = pygame.image.load("map5.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
CAR_COLOR = (200, 50, 50)
RAY_COLOR = (0, 255, 0)
WALL_COLOR = (255, 255, 255)

# Rays
RAY_ANGLES = [-90, -45, 0, 45, 90]

# Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.width = 50
        self.height = 30
        self.MAX_SPEED = 6
        self.ACCEL = 0.2
        self.TURN = 4
        self.FRICTION = 0.05

    def update_position(self):
        # move car
        if self.speed > 0:
            self.speed -= self.FRICTION
        elif self.speed < 0:
            self.speed += self.FRICTION

        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y -= math.sin(math.radians(self.angle)) * self.speed

        # keep inside window
        self.x = max(10, min(WIDTH - 10, self.x))
        self.y = max(10, min(HEIGHT - 10, self.y))

    def get_sensors(self, raw=False):
        cx, cy = self.x, self.y
        distances = []
        for r in RAY_ANGLES:
            angle = self.angle + r
            dist = 0
            while dist < 1000:
                rx = int(cx + math.cos(math.radians(angle)) * dist)
                ry = int(cy - math.sin(math.radians(angle)) * dist)
                if rx < 0 or rx >= WIDTH or ry < 0 or ry >= HEIGHT:
                    break
                if background.get_at((rx, ry))[:3] == (255, 255, 255):
                    break
                dist += 1
            distances.append(dist)
        if raw:
            return distances
        return [d / 1000 for d in distances]

    def check_collision(self):
        cx, cy = int(self.x), int(self.y)
        return background.get_at((cx, cy))[:3] == (255, 255, 255)

    def draw(self, screen):
        car_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        car_surf.fill(CAR_COLOR)
        rotated = pygame.transform.rotate(car_surf, self.angle)
        car_rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, car_rect)

        # draw rays
        for r in RAY_ANGLES:
            ray_angle = self.angle + r
            dist = 0
            while dist < 1000:
                rx = int(self.x + math.cos(math.radians(ray_angle)) * dist)
                ry = int(self.y - math.sin(math.radians(ray_angle)) * dist)
                if rx < 0 or rx >= WIDTH or ry < 0 or ry >= HEIGHT:
                    break
                if background.get_at((rx, ry))[:3] == (255, 255, 255):
                    break
                dist += 1
            rx = int(self.x + math.cos(math.radians(ray_angle)) * dist)
            ry = int(self.y - math.sin(math.radians(ray_angle)) * dist)
            pygame.draw.line(screen, RAY_COLOR, (self.x, self.y), (rx, ry), 2)
            pygame.draw.circle(screen, RAY_COLOR, (rx, ry), 4)


# RL Environment

# Initialize
car = Car(830, 930)
env = DrivingEnv.DrivingEnv(car)
state, _ = env.get_state()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # random action for now
    action = random.randint(0, 4)
    next_state, reward, done = env.step(action)
    state = next_state

    # reset if crashed
    if done:
        car = Car(830, 930)
        env = DrivingEnv(car)
        state, _ = env.get_state()

    # draw everything
    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIDTH, HEIGHT), 5)
    car.draw(screen)
    pygame.display.flip()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False

    print(state, action,reward, done)

pygame.quit()
