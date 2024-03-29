import pygame
import math, random

pygame.mixer.init()

from AssetManager import assetManager
from output import Logger

output = Logger()
AssetManager = assetManager(transform_scale=64)

class Player:

    class Hand:

      def __init__(self, player, radius, color, thickness):
         self.player = player 
         self.radius = radius
         self.color = color
         self.thickness = thickness
         self.angle = 0
         self.position = None
         self.item = None

      def update(self):
        adjusted_radius = self.radius / 2 * 1.8

        hand_x = self.player.center_x + adjusted_radius * math.cos(math.radians(self.angle))
        hand_y = self.player.center_y + adjusted_radius * math.sin(math.radians(self.angle))

        self.position = (int(hand_x), int(hand_y))
    
    def __init__(self, x, y, username="Player"):
        # character
        self.username = username
        self.image = AssetManager.player_front_idle_sprites[0]
        self.x, self.y = x, y
        self.angle = 0
        self.velocity = 2
        self.direction = 0
        self.is_animating = False
        self.current_sprite = 0
        self.sprite_speed = 0.3
        self.animation_state = "idle" # default
        self.facing = "north"
        self.holding_item = None
        self.hitting_object = None # if player.hitting object == None: run hit on self. else: if not player.hitting:object = self: dont do anything since its not you

        # frame speed
        self.walking_frame_speed = 0.3
        self.attack_frame_speed = 0.3
        self.idle_frame_speed = 0.3
        self.damage_frame_speed = 0.2

        # frame counts
        self.sprite_frame_count = 12 # default idle animation
        self.attacking_frame_count = 7
        self.damage_frame_count = 4
        self.idle_frame_count = 12
        self.walking_frame_count = 6

        # rect
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y
        self.size = pygame.Vector2(self.image.get_width(), self.image.get_height())
        self.center_x = self.x + (self.image.get_width() // 2)
        self.center_y = self.y + (self.image.get_height() // 2)
        self.hand = self.Hand(self, radius=20, color=(255, 0, 0), thickness=5)
        
    
    def animate(self):
      self.is_animating = True
      if not self.animation_state == "walking":
        self.update_anim_state("walking")
    
    def keyup(self):
      self.is_animating = False
      self.current_sprite = 0
      self.update_anim_state("idle")
    
    def update_anim_state(self, state):
      self.animation_state = state
      self.current_sprite = 0

    def update(self):

      # only update own position, not blit
      self.hand.angle = self.direction
      self.hand.update()

      if self.current_sprite >= self.idle_frame_count:
          self.current_sprite = 0

      self.direction = self.direction % 360

      # Make sure to account for, for example, changing directions while attacking.
      match self.animation_state:
          # Handling walking animation
          case "walking":
              self.current_sprite += self.walking_frame_speed
              if self.current_sprite >= self.walking_frame_count:
                  self.current_sprite = 0

              if self.direction < -90 or self.direction >= 180:
                  self.image =  AssetManager.player_back_walk_sprites[int(self.current_sprite)]
                  self.facing = "north"
              elif -45 <= self.direction < 45:
                self.image = AssetManager.player_right_walk_sprites[int(self.current_sprite)]
                self.facing = "east"
              elif 0 <= self.direction < 90:
                self.image = AssetManager.player_front_walk_sprites[int(self.current_sprite)]
                self.facing = "south"
              else:
                self.image = AssetManager.player_left_walk_sprites[int(self.current_sprite)]
                self.facing = "west"

          # Handling idle animation
          case "idle":
              self.current_sprite += self.idle_frame_speed
              if self.current_sprite >= self.idle_frame_count:
                  self.current_sprite = 0

              if self.direction < -90 or self.direction >= 180:
                self.image =  AssetManager.player_back_idle_sprites[int(self.current_sprite)]
                self.facing = "north"
              elif -45 <= self.direction < 45:
                self.image = AssetManager.player_right_idle_sprites[int(self.current_sprite)]
                self.facing = "east"
              elif 0 <= self.direction < 90:
                self.image = AssetManager.player_front_idle_sprites[int(self.current_sprite)]
                self.facing = "south"
              else:
                self.image = AssetManager.player_left_idle_sprites[int(self.current_sprite)]
                self.facing = "west"

          # Handling attacking animation
          case "attacking":
              
              if not self.holding_item == None: # code shouldnt reach this, its only a precaution
                 return

              self.current_sprite += self.attack_frame_speed
              if self.current_sprite >= self.attacking_frame_count:
                  self.current_sprite = 0
                
              # audio
              if int(self.current_sprite) == 1:
                random.choice(AssetManager.player_attack_sounds).play() # plays 3 times, fix this. is caused because its 1 for longer than its supposed to.
                # maybe wait the lenght of the sound?

              if self.direction < -90 or self.direction >= 180:
                self.image =  AssetManager.player_back_attack_sprites[int(self.current_sprite)]
                self.facing = "north"
              elif -45 <= self.direction < 45:
                self.image = AssetManager.player_right_attack_sprites[int(self.current_sprite)]
                self.facing = "east"
              elif 0 <= self.direction < 90:
                self.image = AssetManager.player_front_attack_sprites[int(self.current_sprite)]
                self.facing = "south"
              else:
                self.image = AssetManager.player_left_attack_sprites[int(self.current_sprite)]
                self.facing = "west"

          # Handling damage animation
          case "damage":
              self.current_sprite += self.damage_frame_speed
              if self.current_sprite >= self.damage_frame_count:
                  self.current_sprite = 0

              if self.direction < -90 or self.direction >= 180:
                self.image =  AssetManager.player_back_damage_sprites[int(self.current_sprite)]
                self.facing = "north"
              elif -45 <= self.direction < 45:
                self.image = AssetManager.player_right_damage_sprites[int(self.current_sprite)]
                self.facing = "east"
              elif 0 <= self.direction < 90:
                self.image = AssetManager.player_front_damage_sprites[int(self.current_sprite)]
                self.facing = "south"
              else:
                self.image = AssetManager.player_left_damage_sprites[int(self.current_sprite)]
                self.facing = "west"
