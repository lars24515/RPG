from output import Logger
import pygame
import os

logger = Logger()

pygame.display.set_mode((1, 1), pygame.NOFRAME)

class assetManager:
      
      def __init__(self, transform_scale=64):
         self.transform_scale = transform_scale

         # items
         self.item_images = self.get_assets("./Sprites/Items", transform=True, list=False, custom_scale=32)
         self.item_bg = pygame.transform.scale(pygame.image.load("./Sprites/item_background.png").convert_alpha(), (32, 32))

         # environment
         self.resources = self.get_assets("./Sprites/Resources", transform=True, list=False)
         self.grass_sprites = self.get_assets("./Sprites/Resources/Grass", transform=True, list=True)
         self.tree_img = pygame.image.load("./Sprites/Resources/forest.png").convert_alpha()
         self.night = pygame.image.load("./Sprites/Enviroment/night.png").convert_alpha()
         self.rain_sprites = self.get_assets("./Sprites/Enviroment/Rain", transform=False, list=True) # render in center of screen

         # audio
         self.footstep_sounds = self.get_assets("./Audio/Player/Footsteps", transform=False, list=True)
         self.set_volume(self.footstep_sounds, 0.1)
         self.player_sounds = self.get_assets("./Audio/Player", transform=False, list=False)
         self.environment_sounds = self.get_assets("./Audio/Environment", transform=False, list=False)
         self.environment_sounds["ambience"].set_volume(0.3)
         self.environment_sounds["rain"].set_volume(1)
         self.player_attack_sounds = self.get_assets("./Audio/Player/Attack", transform=False, list=True)
         self.set_volume(self.player_attack_sounds, 0.4)

         # player sprites
         
         # front
         self.player_front_idle_sprites = self.get_assets("./Sprites/Player/Front/Idle", transform=True, list=True, custom_scale=128)
         self.player_front_walk_sprites = self.get_assets("./Sprites/Player/Front/Walk", transform=True, list=True, custom_scale=128)
         self.player_front_attack_sprites = self.get_assets("./Sprites/Player/Front/Attack", transform=True, list=True, custom_scale=128)
         self.player_front_damage_sprites = self.get_assets("./Sprites/Player/Front/Damage", transform=True, list=True, custom_scale=128)

         # back
         self.player_back_idle_sprites = self.get_assets("./Sprites/Player/Back/Idle", transform=True, list=True, custom_scale=128)
         self.player_back_walk_sprites = self.get_assets("./Sprites/Player/Back/Walk", transform=True, list=True, custom_scale=128)
         self.player_back_attack_sprites = self.get_assets("./Sprites/Player/Back/Attack", transform=True, list=True, custom_scale=128)
         self.player_back_damage_sprites = self.get_assets("./Sprites/Player/Back/Damage", transform=True, list=True, custom_scale=128)

         # left
         self.player_left_idle_sprites = self.get_assets("./Sprites/Player/Left/Idle", transform=True, list=True, custom_scale=128)
         self.player_left_walk_sprites = self.get_assets("./Sprites/Player/Left/Walk", transform=True, list=True, custom_scale=128)
         self.player_left_attack_sprites = self.get_assets("./Sprites/Player/Left/Attack", transform=True, list=True, custom_scale=128)
         self.player_left_damage_sprites = self.get_assets("./Sprites/Player/Left/Damage", transform=True, list=True, custom_scale=128)

         # right
         self.player_right_idle_sprites = self.get_assets("./Sprites/Player/Right/Idle", transform=True, list=True, custom_scale=128)
         self.player_right_walk_sprites = self.get_assets("./Sprites/Player/Right/Walk", transform=True, list=True, custom_scale=128)
         self.player_right_attack_sprites = self.get_assets("./Sprites/Player/Right/Attack", transform=True, list=True, custom_scale=128)
         self.player_right_damage_sprites = self.get_assets("./Sprites/Player/Right/Damage", transform=True, list=True, custom_scale=128)

      def set_volume(self, list, volume):
          for sound in list:
             sound.set_volume(volume)

      def get_assets(self, path, transform=True, list=False, custom_scale=None):
         os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
         new_map = {}
         newList = []
         #logger.info(f"Loading files for {path}..", "AssetManager")
         
         for fileName in os.listdir(path):
            if fileName.endswith(".png"):
                  filePath = os.path.join(path, fileName)
                  image = pygame.image.load(filePath).convert_alpha()
                  name = fileName.split(".")[0]

                  if transform:
                     
                     if not custom_scale:
                        image = pygame.transform.scale(image, (self.transform_scale, self.transform_scale))
                     else:
                        image = pygame.transform.scale(image, (custom_scale, custom_scale))

                  if not list:
                     new_map[name] = image
                  else: # its a list
                     newList.append(image)

                  #logger.info(f"loaded {fileName} with transform {transform}", "AssetManager")
                     
            elif fileName.endswith(".mp3"):
                filePath = os.path.join(path, fileName)
                sound = pygame.mixer.Sound(filePath)
                name = fileName.split(".")[0]

                if not list:
                    new_map[name] = sound
                else:  # its a list
                    newList.append(sound)

         #logger.success(f"loaded all files from {path}", "AssetManager")

         if not list:
            return new_map
         else:
            return newList