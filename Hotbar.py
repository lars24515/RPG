from colors import Colors
from output import Logger
from AssetManager import assetManager

Colors = Colors()
output = Logger()
AssetManager = assetManager()

def axe_callback(self):
    output.info("axe callback", "Hotbar")

item_callbacks = {
    "Axe": axe_callback
}

class Item:

    def __init__(self, name, count):
        self.name, self.count = name, count
        self.cateogry = "" # index a category dict or smt; placable, consumable, etc.
        self.callback = item_callbacks[self.name]
        self.image = AssetManager.item_images[self.name]
        self.stack = 1

class Hotbar:
    def __init__(self, x, y, start_items: dict = {}):
        self.x, self.y = x, y
        self.item_slots = 10
        self.slot_size = 40
        self.selected_slot = 1
        # dont use individual images for slots
        # render in start without slot image
        self.items = start_items # {"obj_name": class_obj}

    def update_selector(self, selected_slot):
        border_thickness = 3 
        selector_color = Colors.white

        selector_x = self.x + self.slot_size * selected_slot
        selector_y = self.y
        selector_width = self.slot_size
        selector_height = self.slot_size

        #pygame.draw.rect(screen, selector_color, (selector_x, selector_y, selector_width, selector_height), border_thickness)

    def add_item(self, item_object, count=1):
        if item_object.name not in self.items:
            self.items[item_object.name] = item_object
            output.info(f"Added {item_object.name} to hotbar", "Hotbar")
        else: # item already in inventry
            output.info(f"{item_object.name} already in hotbar, increased stack to {self.items[item_object.name].stack + count}", "Hotbar")
            self.items[item_object.name].stack += count
    
    # render items from game loop