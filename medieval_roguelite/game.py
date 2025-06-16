"""Simple medieval-themed roguelite platformer."""

import sys
import pygame
from .levels import LEVELS, WIDTH, HEIGHT, GRAVITY
from .items import Item

PLAYER_SIZE = (40, 60)
PLAYER_COLOR = (50, 205, 50)  # lime green

class Player:
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], *PLAYER_SIZE)
        self.vel_y = 0
        self.items = []

    def move(self, dx, dy, level):
        # horizontal movement
        self.rect.x += dx
        for block in level.ground_rects:
            if self.rect.colliderect(block):
                if dx > 0:
                    self.rect.right = block.left
                elif dx < 0:
                    self.rect.left = block.right
        # vertical movement
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y + dy
        for block in level.ground_rects:
            if self.rect.colliderect(block):
                if self.vel_y > 0:
                    self.rect.bottom = block.top
                    self.vel_y = 0
                elif self.vel_y < 0:
                    self.rect.top = block.bottom
                    self.vel_y = 0

    def jump(self, level):
        # Only jump if standing on something
        self.rect.y += 1
        on_ground = any(self.rect.colliderect(b) for b in level.ground_rects)
        self.rect.y -= 1
        if on_ground:
            self.vel_y = -10

    def draw(self, surf):
        pygame.draw.rect(surf, PLAYER_COLOR, self.rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Medieval Roguelite")
        self.clock = pygame.time.Clock()
        self.current_level = 0
        self.player = Player((50, HEIGHT - 100))

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.jump(LEVELS[self.current_level])

            keys = pygame.key.get_pressed()
            dx = 0
            if keys[pygame.K_LEFT]:
                dx = -5
            if keys[pygame.K_RIGHT]:
                dx = 5

            self.player.move(dx, 0, LEVELS[self.current_level])
            self.check_items()
            self.check_level_end()
            self.draw()
        pygame.quit()
        sys.exit()

    def check_items(self):
        level = LEVELS[self.current_level]
        for pos, item in list(level.items.items()):
            item_rect = pygame.Rect(pos[0] - 10, pos[1] - 10, 20, 20)
            if self.player.rect.colliderect(item_rect):
                self.player.items.append(item)
                del level.items[pos]

    def check_level_end(self):
        # If player reaches right edge, go to next level
        if self.player.rect.right >= WIDTH - 10:
            self.current_level += 1
            if self.current_level >= len(LEVELS):
                print("You Win! Collected items:")
                for it in self.player.items:
                    print("-", it.name)
                pygame.time.wait(2000)
                pygame.quit()
                sys.exit()
            self.player.rect.x = 50
            self.player.rect.y = HEIGHT - 100

    def draw(self):
        self.screen.fill((135, 206, 235))  # sky blue
        level = LEVELS[self.current_level]
        level.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    Game().run()
