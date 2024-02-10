import pygame
import sys, random, math, os
import numpy as np
from perlin_noise import PerlinNoise
import time

from output import Logger
from player import Player
from AssetManager import assetManager
from Tile import Tile
from colors import Colors
from Environment import Environment
from Hotbar import Hotbar
from Hotbar import Item

pygame.mixer.init()

output = Logger()
AssetManager = assetManager(transform_scale=64)
Colors = Colors()
Environment = Environment()
Hotbar = Hotbar( ( (1000 // 2) - ((10*40) // 2) ) , 20, start_items={  })


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

'''

 -- footsteps

 play the footstep sound in a random pitch

test from school computer

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
    self.items = { } {"banana": class_obj}

    def add_item(self, item, amount=1): # default amount 1 if not specified
        if item.name not in self.items:
            self.items.insert({item.name}: item)
        else: # item is already in inventory
            self.items[item.name].stack += amount
    
    def render(self):
        for item, index in enumerate(self.items):
            game.draw(self.slot_image, x = index*slotsize or something idk man)

self.trees = [ (100, 100) = {"image": tree_breaking_img} ]

to do:

dynamic day/night cycle and weather; 12:00 to 24:00 gradual change (opacity)
( make it so a time corresponds to an opacity value )
make trees 2 tiles tall
hotbar
items
tile interaction

'''

class Game:
    def __init__(self, WIDTH, HEIGHT, VIEWPORT_WIDTH, VIEWPORT_HEIGHT):
        self.tile_size = AssetManager.transform_scale
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        self.WIDTH, self.HEIGHT, self.TILESIZE = WIDTH, HEIGHT, self.tile_size
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        # since then i can set positions beforehand, and then update the tile
        # object once it is rendered by the player? old
        self.tiles = pygame.sprite.Group()
        self.player = Player( (self.WIDTH // 2) - (AssetManager.player_front_idle_sprites[0].get_width() // 2), (self.HEIGHT // 2) - (AssetManager.player_front_idle_sprites[0].get_height() // 2) , "lars")
        self.clock = pygame.time.Clock()
        self.noise = PerlinNoise(octaves=5, seed=random.randint(0, 100))
        self.scale = 0.05
        self.VIEWPORT_WIDTH = VIEWPORT_WIDTH
        self.VIEWPORT_HEIGHT = VIEWPORT_HEIGHT
        self.viewport_x = self.WIDTH // 2 - self.VIEWPORT_WIDTH // 2
        self.viewport_y = self.HEIGHT // 2 - self.VIEWPORT_HEIGHT // 2
        self.visible_tiles = set()
        self.loading_progress = 0
        self.world_size = 40
        self.total_tiles = self.world_size*self.world_size
        self.center_x, self.center_y = self.WIDTH // 2, self.HEIGHT // 2
        pygame.font.init()
        self.font = pygame.font.Font("./Fonts/AurulentSansMNerdFont-Regular.otf", 20)
        self.save_performance = False
        self.threshold_distance = 70
        self.close_tiles = pygame.sprite.Group()
        self.footstep_cooldown = 0  # Cooldown time in seconds
        self.footstep_cooldown_duration = 0.25  # Adjust as needed
        self.last_frame_time = time.time()
        self.debugging_mode = True
        if self.save_performance:
            self.world_size = 0

    def draw(self, img, x, y, opacity=255):
        img.set_alpha(opacity)
        self.screen.blit(img, (x, y))
    
    def exit(self):
        self.running = False
        sys.exit()
    
    def draw_progress_bar(self, screen):
        progress_width = self.WIDTH * (self.loading_progress / self.total_tiles)
        pygame.draw.rect(screen, GREEN, (0, self.HEIGHT - 20, progress_width, 20))
        pygame.display.update()
    
    def generate_world_around_player(self):
        for x in range(-self.world_size, self.world_size):
            for y in range(-self.world_size, self.world_size):
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
                    tile_type = "tree"
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

    def render_hotbar_items(self):
        Hotbar.update_selector()
        for index, (item_name, item_obj) in enumerate(Hotbar.items.items()):
            item_x = Hotbar.x + index * Hotbar.slot_size
            position = (item_x, Hotbar.y)
            self.screen.blit(AssetManager.item_bg, position) # render background
            self.screen.blit(item_obj.image, position)
            text_surface = self.font.render(str(item_obj.stack), True, Colors.white)  
            # Render outline of the stack text
            text_surface_outline = self.font.render(str(item_obj.stack), True, Colors.black)  
            self.draw(text_surface_outline, (item_x + item_obj.image.get_width() - 5) + 1, Hotbar.y - (text_surface_outline.get_height() // 2) + 1)
    
            # Render the stack text
            text_surface = self.font.render(str(item_obj.stack), True, Colors.white)  
            self.draw(text_surface, item_x + item_obj.image.get_width() - 5, Hotbar.y - (text_surface.get_height() // 2))
            # class for displaying text with opacity. draw image then add negative value to opacity gradually
            
            if Hotbar.selected_slot > 0:
                pygame.draw.ellipse(self.screen, Colors.white, (Hotbar.selector_x - 4, Hotbar.selector_y - 4, Hotbar.selector_width, Hotbar.selector_height), 3)

    def handle_hotbar_input(self, key):

        if Hotbar.selected_slot and Hotbar.selected_slot == key:
            Hotbar.selected_slot = 0 # un-equip an item
            self.player.holding_item = None
            AssetManager.player_sounds["unequip"].play()
            return

        keys_list = list(Hotbar.items.keys())
        if 0 <= key - 1 < len(keys_list) and keys_list[key - 1] is not None:
            Hotbar.selected_slot = key
            selected_item_name = keys_list[key - 1]
            selected_item_obj = Hotbar.items[selected_item_name]
            self.player.holding_item = selected_item_obj  
            AssetManager.player_sounds["equip"].play()


    def handle_keydown(self, event):

        if event.key == pygame.K_ESCAPE:
            self.exit()
            return # hopefully the code wont reach this line

        key = event.key - pygame.K_0
        if 1 <= key <= 9:
            self.handle_hotbar_input(key)
            return
        
        # other binds

    def handle_sound(self, dt):
        # dt represents the time passed since the last frame update
        if self.player.animation_state == "walking":
            if self.footstep_cooldown <= 0:
                sound = random.choice(AssetManager.footstep_sounds)
                sound.play()
                self.footstep_cooldown = self.footstep_cooldown_duration
            else:
                self.footstep_cooldown -= dt
    
    def clicking(self, sprite):
        return sprite.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]
    
    def handle_sprite_click(self, sprite):
        output.info("clicked", sprite.element)
        if not hasattr(sprite, "element") or sprite.element == "grass" or sprite.element == "water": # means sprite is a tile, and not for example player
            return
        
        # if player is holding an item, then hitpoint removal will be 1. but it player is holding an item, it will depend 
        # on the type of item. index a dict to see how many.

        if sprite.hit_points > 1:
            
            if self.player.holding_item == None: # player is using hand
                sprite.hit_points -= 1
            else:
                if hasattr(self.player.holding_item, "category"):
                    if self.player.holding_item.category in Hotbar.category_callbacks:
                        sprite.hit_points -= 2 # this means that if the item player is holding is a tool then it will be 2 damage.
                        # rework this later using a "tool" category which will be much easier
                        # i just dont wanna work on it right now

    def run(self):
        self.generate_world_around_player()
        AssetManager.environment_sounds["ambience"].play(-1)
        Hotbar.add_item(Item("wooden_sword", 1))
        Hotbar.add_item(Item("wooden_pickaxe", 1))
        Hotbar.add_item(Item("wooden_axe", 1))
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()
                
                # input
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button

                        if self.player.holding_item == None:
                            self.player.animate()
                            self.player.update_anim_state("attacking")
                        
                        # other binds

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left mouse button
                        self.player.update_anim_state("idle") # when idling while holding item, this will reset idle animation. not first priority.
                        self.player.is_animating = False
                    
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

                # other
                        
                keys = pygame.key.get_pressed()

                if keys[pygame.K_w]:
                    self.player.animate()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player.keyup()

            # general code

            self.screen.fill((144, 238, 144))

            mouse_position = pygame.Vector2(pygame.mouse.get_pos())
            dx = mouse_position.x - self.player.rect.x 
            dy = mouse_position.y - self.player.rect.y  # if self.player.anim_state == "hitting" and player.hit_progress == 100 ( make it so that like a 60 degree axe image angle == 100 progress )
            angle = math.atan2(dy, dx)
            angle_degrees = math.degrees(angle)
            self.player.direction = angle_degrees

            self.player.update()
            
            self.viewport_x = max(0, min(self.player.x - self.VIEWPORT_WIDTH // 2, self.WIDTH - self.VIEWPORT_WIDTH)) - 60
            self.viewport_y = max(0, min(self.player.y - self.VIEWPORT_HEIGHT // 2, self.HEIGHT - self.VIEWPORT_HEIGHT)) - 60

            self.tiles.update(self.player, self.screen, self.viewport_x, self.viewport_y, self.VIEWPORT_HEIGHT, self.VIEWPORT_WIDTH)
    
            self.draw(self.player.image, self.player.x, self.player.y)


            self.close_tiles.empty()

            for tile in self.tiles:
                tile_distance_to_player = pygame.math.Vector2(tile.rect.center).distance_to(self.player.rect.center)
                if tile_distance_to_player < self.threshold_distance and tile.element == "tree":
                    self.close_tiles.add(tile)


            # check if close tiles are colliding with player hitbox
            colliding_tiles = pygame.sprite.spritecollide(self.player, self.close_tiles, False)
            if colliding_tiles:
                for sprite in colliding_tiles:
                    if self.debugging_mode:
                        text_surface = self.font.render(sprite.element, True, (255, 0, 0))  # Render text surface
                        self.screen.blit(text_surface, (sprite.rect.x, sprite.rect.y - text_surface.get_height()))
                        pygame.draw.rect(self.screen, (255, 0, 0), sprite.rect, width=3)

                    # iterating through each tile player is colliding with:
                    
                    if self.clicking(sprite):
                        if not self.player.hitting_object == sprite:
                            self.player.hitting_object = sprite
                            self.handle_sprite_click(sprite)

            if self.debugging_mode:
                text_surface = self.font.render("player hitbox", True, (255, 0, 0))  # Render text surface
                self.screen.blit(text_surface, (self.player.rect.x, self.player.rect.y - text_surface.get_height()))
                pygame.draw.rect(self.screen, (255, 0, 0), self.player.rect, width=3)

            if not self.player.holding_item == None: # player is holding an item
                self.screen.blit(self.player.holding_item.image, self.player.hand.position)
                # if angle > 90 flip imaeg

            # audio

            current_time = time.time()
            dt = current_time - self.last_frame_time
            self.last_frame_time = current_time  # Update last frame time for the next iteration

            # Call the handle_sound() function and pass dt
            self.handle_sound(dt)

            # time
            Environment.day_night_cycle()
            Environment.weather_cycle()
            
            # draw night on top of weather
            if not self.save_performance:
                if Environment.weather_image != None:
                    self.draw(Environment.weather_image, self.center_x - Environment.weather_image.get_width() // 2, self.center_y - Environment.weather_image.get_height() // 2)
                self.draw(AssetManager.night, self.center_x - AssetManager.night.get_width() // 2, self.center_y - AssetManager.night.get_height() // 2, opacity=Environment.night_opacity)
            
            self.render_hotbar_items()

            # debugging
            
            if self.debugging_mode:
                text_surface = self.font.render(f"animation_state: {self.player.animation_state}", True, (255, 255, 255))  # Render text surface
                self.screen.blit(text_surface, (10, 10))
                text_surface = self.font.render(f"direction: {int(self.player.direction)}", True, (255, 255, 255))  # Render text surface
                self.screen.blit(text_surface, (10, 37))
                text_surface = self.font.render(f"facing: {self.player.facing}", True, (255, 255, 255))  # Render text surface
                self.screen.blit(text_surface, (10, 64))
                text_surface = self.font.render(f"time: {Environment.time_string}", True, (255, 255, 255))  # Render text surface
                self.screen.blit(text_surface, (10, 91))
                text_surface = self.font.render(f"weather: {Environment.current_weather}", True, (255, 255, 255))  # Render text surface
                self.screen.blit(text_surface, (10, 118))
                text_surface = self.font.render(f"colliding with {len(colliding_tiles)} sprites", True, (255, 255, 255))  # Render text surface
                self.screen.blit(text_surface, (10, 145))

            self.clock.tick(60)
            fps = int(self.clock.get_fps())
            pygame.display.set_caption(f"RPG Game - [CLIENT] - FPS: {fps}")


            pygame.display.update()

game = Game(1000, 600, 1100, 800)

game.run()