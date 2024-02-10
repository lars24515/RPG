from colors import Colors
from output import Logger
from AssetManager import assetManager

Colors = Colors()
output = Logger()
AssetManager = assetManager()

def axe_callback(self):
    output.info("axe callback", "Hotbar")

def sword_callback(self):
    output.info("sword callback", "Hotbar")

def pickaxe_callback(self):
    output.info("pickaxe callback", "Hotbar")


class Item:

    def __init__(self, name, count):
        self.name, self.count = name, count
        self.cateogry = self.name.split("_")[1] # assuming its "material_objecttype"
        self.type = "" # index dict ( Axe, sword, etc. for different type of materials ) --> callbacks
        self.callback = Hotbar.category_callbacks[self.name.split("_")[1]] # assuming its "material_objecttype"
        self.image = AssetManager.item_images[self.name]
        self.stack = 1

class Hotbar:
    category_callbacks = {
        "axe": axe_callback,
        "sword": sword_callback,
        "pickaxe": pickaxe_callback,
    }
    def __init__(self, x, y, start_items: dict = {}):
        self.x, self.y = x, y
        self.item_slots = 10
        self.slot_size = 40
        self.selected_slot = 0
        # dont use individual images for slots
        # render in start without slot image
        self.items = start_items # {"obj_name": class_obj}
        

    def update_selector(self):
        self.selector_x = self.x + self.slot_size * (self.selected_slot - 1)
        self.selector_y = self.y
        self.selector_width = self.slot_size
        self.selector_height = self.slot_size

    def add_item(self, item_object, count=1):
        if item_object.name not in self.items:
            self.items[item_object.name] = item_object
            output.info(f"Added {item_object.name} to hotbar", "Hotbar")
            AssetManager.player_sounds["equip"].play()
        else: # item already in inventry
            output.info(f"{item_object.name} already in hotbar, increased stack to {self.items[item_object.name].stack + count}", "Hotbar")
            self.items[item_object.name].stack += count
            AssetManager.player_sounds["equip"].play()
    
    # render items from game loop