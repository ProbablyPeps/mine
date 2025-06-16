import pygame
from .items import random_item

WIDTH = 800
HEIGHT = 600
GRAVITY = 0.5

class Level:
    def __init__(self, ground_rects, item_positions):
        self.ground_rects = ground_rects
        # Each item position will store the item currently spawned there
        self.item_positions = item_positions
        self.items = {pos: random_item() for pos in item_positions}

    def draw(self, surf):
        for rect in self.ground_rects:
            pygame.draw.rect(surf, (139, 69, 19), rect)  # brown blocks
        for pos, item in self.items.items():
            pygame.draw.circle(surf, (255, 215, 0), pos, 10)

# Define three simple levels
LEVELS = []

# Level 1: simple flat ground
level1_ground = [pygame.Rect(0, HEIGHT - 40, WIDTH, 40)]
level1_items = [(200, HEIGHT - 60), (400, HEIGHT - 60), (600, HEIGHT - 60)]
LEVELS.append(Level(level1_ground, level1_items))

# Level 2: a few platforms
level2_ground = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(150, HEIGHT - 150, 100, 20),
    pygame.Rect(350, HEIGHT - 250, 100, 20),
    pygame.Rect(550, HEIGHT - 350, 100, 20),
]
level2_items = [(175, HEIGHT - 170), (375, HEIGHT - 270), (575, HEIGHT - 370)]
LEVELS.append(Level(level2_ground, level2_items))

# Level 3: more platforms
level3_ground = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(100, HEIGHT - 200, 100, 20),
    pygame.Rect(300, HEIGHT - 300, 100, 20),
    pygame.Rect(500, HEIGHT - 400, 100, 20),
    pygame.Rect(650, HEIGHT - 500, 100, 20),
]
level3_items = [(125, HEIGHT - 220), (325, HEIGHT - 320), (525, HEIGHT - 420)]
LEVELS.append(Level(level3_ground, level3_items))
