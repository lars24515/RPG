import pygame
import sys, random, math, os
import numpy as np
from perlin_noise import PerlinNoise

from output import Logger
from player import Player
from AssetManager import assetManager
from Tile import Tile
from colors import Colors

output = Logger()
AssetManager = assetManager(transform_scale=64)
Colors = Colors()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

'''

def sugar_callback():
    print("this is sugar")

item_callback_map = {
    "sugar": sugar_callback
}

class Item:

    def __init__(self, name):
        self.name = name
        self.stack = 1
        self.callback = item_callback_map[self.name]
        self.image = AssetManager.items[self.name]
    
class Hotbar:
    def __init__(self, x, y):
    self.x, self.y = x, y
    self.slots = 10
    self.slot_size = 40
    self.slot_image = AssetManager.slot_image
    self.rect pygame.Rect(len(self.items) * self.slot_size) ellerno
    self.items = { } {"banana": item_obj}
    self.current_item_types = ["apple", "banana"]

    def add_item(self, item, amount=1): # default amount 1 if not specified
        if item.name not in self.current_item_types:
            self.current_item_types.append(item.name)
            self.items.insert({item.name}: item)
        else: # item is already in inventory
            self.items[item.name].stack += amount
    
    def render(self):
        for item, index in enumerate(self.items):
            game.draw(self.slot_image, x = index*slotsize veit da fan)

self.trees = [ (100, 100) = {"image": tree_breaking_img} ]

'''

class Game:
    def __init__(self, WIDTH, HEIGHT, VIEWPORT_WIDTH=1050, VIEWPORT_HEIGHT=650):
        self.tile_size = AssetManager.transform_scale
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.WIDTH, self.HEIGHT, self.TILESIZE = WIDTH, HEIGHT, self.tile_size
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        # since then i can set positions beforehand, and then update the tile
        # object once it is rendered by the player? old
        self.tiles = pygame.sprite.Group()
        self.player = Player((self.WIDTH // 2), (self.HEIGHT // 2), "lars")
        self.clock = pygame.time.Clock()
        self.noise = PerlinNoise(octaves=5, seed=random.randint(0, 100))
        self.scale = 0.05
        self.VIEWPORT_WIDTH = VIEWPORT_WIDTH
        self.VIEWPORT_HEIGHT = VIEWPORT_HEIGHT
        self.viewport_x = max(0, min(self.player.x - self.VIEWPORT_WIDTH // 2, self.WIDTH - self.VIEWPORT_WIDTH))
        self.viewport_y = max(0, min(self.player.y - self.VIEWPORT_HEIGHT // 2, self.HEIGHT - self.VIEWPORT_HEIGHT))
        self.visible_tiles = set()
        self.loading_progress = 0
        self.total_tiles = 10 * 10
        self.tile_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.tile_surface.set_colorkey(BLACK) # set bg to black

    def draw(self, img, x, y):
        self.screen.blit(img, (x, y))
    
    def exit(self):
        self.running = False
        sys.exit()
    
    def draw_progress_bar(self, screen):
        progress_width = self.WIDTH * (self.loading_progress / self.total_tiles)
        pygame.draw.rect(screen, GREEN, (0, self.HEIGHT - 20, progress_width, 20))
        pygame.display.update()
    
    def generate_world_around_player(self):
        for x in range(-10, 10):
            for y in range(-10, 10):
                noise_val = self.noise([x * self.scale, y * self.scale])

                # Calculate actual coordinates for the tile
                tile_x = x * self.tile_size
                tile_y = y * self.tile_size

                # Example: Assign different tiles based on noise value
                if noise_val < -0.2:
                    tile_type = "water"
                elif noise_val < 0.2:
                    tile_type = "grass"
                elif noise_val < 0.5:
                    tile_type = "forest"
                else:
                    tile_type = "mountain"

                # Create tile based on type
                new_tile = Tile(tile_x, tile_y, tile_type)
                self.tiles.add(new_tile)

                self.loading_progress +=1
                self.draw_progress_bar(self.screen)
                a = self.loading_progress / self.total_tiles
                a *= 100
                pygame.display.set_caption(f"RPG Game - [CLIENT] Map: {int(a)}%")

    def run(self):
        self.generate_world_around_player()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                
                # input
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.player.animate(angle_degrees)
                        self.player.update_anim_state("attacking")
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        self.player.update_anim_state("idle")
                        self.player.is_animating = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit()
                
                # other
                        
                keys = pygame.key.get_pressed()

                if keys[pygame.K_w]:
                    self.player.animate(angle_degrees)
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.keyup()

                    
            
            # general code

            self.screen.fill((144, 238, 144))
            

            mouse_position = pygame.Vector2(pygame.mouse.get_pos())

            dx = mouse_position.x - self.player.x
            dy = mouse_position.y - self.player.y
            angle = math.atan2(dy, dx)
            angle_degrees = math.degrees(angle)
            self.player.angle = angle_degrees

            self.player.update()
            
            self.viewport_x = max(0, min(self.player.x - self.VIEWPORT_WIDTH // 2, self.WIDTH - self.VIEWPORT_WIDTH)) - 60
            self.viewport_y = max(0, min(self.player.y - self.VIEWPORT_HEIGHT // 2, self.HEIGHT - self.VIEWPORT_HEIGHT)) - 60

            self.tiles.update(self.player, self.screen, self.viewport_x, self.viewport_y, self.VIEWPORT_HEIGHT, self.VIEWPORT_WIDTH)
            
            self.draw(self.player.image, self.player.x, self.player.y)
            # player hand
            pygame.draw.circle(self.screen, Colors.black, self.player.hand.position, self.player.hand.thickness + 2)
            pygame.draw.circle(self.screen, Colors.white, self.player.hand.position, self.player.hand.thickness)

            self.clock.tick(60)
            fps = int(self.clock.get_fps())
            pygame.display.set_caption(f"RPG Game - [CLIENT] - FPS: {fps}")


            pygame.display.update()

game = Game(1000, 600)

game.run()