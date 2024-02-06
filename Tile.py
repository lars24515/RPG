import pygame
import random, math

from AssetManager import assetManager
from output import Logger

AssetManager = assetManager(transform_scale=64)
output = Logger()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.x, self.y = x, y
        self.element = type
        if self.element == "grass":
            self.image = random.choice(AssetManager.grass_sprites)
        elif self.element == "tree":
            self.image = AssetManager.tree_img
            self.y -= (self.image.get_height() // 2)
        else:
            self.image = AssetManager.resources[type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def draw(self, screen):
        # Draw the tile onto the screen
        screen.blit(self.image, (self.rect.x, self.y))
    
    def update(self, player, screen, viewport_x, viewport_y, VIEWPORT_HEIGHT, VIEWPORT_WIDTH):
        if self.rect == None:
            return # cant access code 
        
        if player.is_animating and player.animation_state == "walking":

            move_distance = player.velocity
            move_angle = math.radians(player.direction)

            delta_x = move_distance * math.cos(move_angle)
            delta_y = move_distance * math.sin(move_angle)

            self.x -= delta_x
            self.y -= delta_y
            self.rect.x, self.rect.y = self.x, self.y


        if viewport_x <= self.rect.x <= viewport_x + VIEWPORT_WIDTH \
        and viewport_y <= self.rect.y <= viewport_y + VIEWPORT_HEIGHT: #inside viewport
            self.draw(screen)
            