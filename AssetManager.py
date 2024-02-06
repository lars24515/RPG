from output import Logger
import pygame
import os

logger = Logger()

pygame.display.set_mode((1, 1), pygame.NOFRAME)

class assetManager:
      
      def __init__(self, transform_scale):
         self.transform_scale = transform_scale
         self.resources = self.get_images("./Sprites/Resources", transform=True, list=False)
         self.grass_sprites = self.get_images("./Sprites/Resources/Grass", transform=True, list=True)
         self.tree_img = pygame.image.load("./Sprites/Resources/forest.png").convert_alpha()
         self.night = pygame.image.load("./Sprites/Enviroment/night.png").convert_alpha()
         self.rain_sprites = self.get_images("./Sprites/Enviroment/Rain", transform=False, list=True) # render in center of screen

         # player sprites
         
         # front
         self.player_front_idle_sprites = self.get_images("./Sprites/Player/Front/Idle", transform=True, list=True, custom_scale=128)
         self.player_front_walk_sprites = self.get_images("./Sprites/Player/Front/Walk", transform=True, list=True, custom_scale=128)
         self.player_front_attack_sprites = self.get_images("./Sprites/Player/Front/Attack", transform=True, list=True, custom_scale=128)
         self.player_front_damage_sprites = self.get_images("./Sprites/Player/Front/Damage", transform=True, list=True, custom_scale=128)

         # back
         self.player_back_idle_sprites = self.get_images("./Sprites/Player/Back/Idle", transform=True, list=True, custom_scale=128)
         self.player_back_walk_sprites = self.get_images("./Sprites/Player/Back/Walk", transform=True, list=True, custom_scale=128)
         self.player_back_attack_sprites = self.get_images("./Sprites/Player/Back/Attack", transform=True, list=True, custom_scale=128)
         self.player_back_damage_sprites = self.get_images("./Sprites/Player/Back/Damage", transform=True, list=True, custom_scale=128)

         # left
         self.player_left_idle_sprites = self.get_images("./Sprites/Player/Left/Idle", transform=True, list=True, custom_scale=128)
         self.player_left_walk_sprites = self.get_images("./Sprites/Player/Left/Walk", transform=True, list=True, custom_scale=128)
         self.player_left_attack_sprites = self.get_images("./Sprites/Player/Left/Attack", transform=True, list=True, custom_scale=128)
         self.player_left_damage_sprites = self.get_images("./Sprites/Player/Left/Damage", transform=True, list=True, custom_scale=128)

         # right
         self.player_right_idle_sprites = self.get_images("./Sprites/Player/Right/Idle", transform=True, list=True, custom_scale=128)
         self.player_right_walk_sprites = self.get_images("./Sprites/Player/Right/Walk", transform=True, list=True, custom_scale=128)
         self.player_right_attack_sprites = self.get_images("./Sprites/Player/Right/Attack", transform=True, list=True, custom_scale=128)
         self.player_right_damage_sprites = self.get_images("./Sprites/Player/Right/Damage", transform=True, list=True, custom_scale=128)





      def get_images(self, path, transform=True, list=False, custom_scale=None):
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

         #logger.success(f"loaded all files from {path}", "AssetManager")

         if not list:
            return new_map
         else:
            return newList