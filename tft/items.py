import random
import json
import copy

ALL_ITEMS = []

class Item:
  def __init__(self, name, component_names=[], consumable=False, emblem=False):
    self.name = name
    self.component_names = component_names
    self.components = [] # Filled by self.compile_components
    self.consumable = consumable
    self.emblem = emblem

  def is_composite(self):
    return not self.is_consumable() and not self.is_emblem() and len(self.components) > 0

  def is_simple(self):
    return not self.is_consumable() and len(self.components) == 0

  def is_consumable(self):
    return self.consumable

  def is_emblem(self):
    return self.emblem

  def compile_components(self):
    for item in ALL_ITEMS:
      if item.name in self.component_names:
        self.components.append(item)

  def __eq__(self, other):
    return isinstance(other, Item) and self.name == other.name

  def __repr__(self):
    return self.name

  @staticmethod
  def get_all():
    return copy.deepcopy(ALL_ITEMS)

  @staticmethod
  def from_name(name):
    for item in ALL_ITEMS:
      if item.name == name:
        return copy.deepcopy(item)
    raise Exception(f"Could'nt find item with name {name}")

  @staticmethod
  def get_random(count=1, simple_only=False, composite_only=False, consumables_only=False, consumables_allowed=False, emblems_allowed=False):
    eligible_items = []
    for item in ALL_ITEMS:
      if consumables_only:
        if item.is_consumable(): eligible_items.append(item)
      elif simple_only:
        if item.is_simple(): eligible_items.append(item)
      elif composite_only:
        if item.is_composite(): eligible_items.append(item)
      else:
        specific_allowed = (consumables_allowed and item.is_consumable()) or (emblems_allowed and item.is_emblem())
        general_allowed = not item.is_emblem() and not item.is_consumable()
        if specific_allowed or general_allowed:
          eligible_items.append(item)
    
    return copy.deepcopy(random.sample(eligible_items, count))

  @staticmethod
  def get_composition(a, b):
    for item in ALL_ITEMS:
      if a in item.components and b in item.components:
        return item
    raise Exception(f"Could'nt find composition with {a} and {b}")

# Loading data on load file
def initialize_items():
  global ALL_ITEMS
  json_file = open("tft/data/items.json", "r")
  items_data = json.load(json_file)

  ALL_ITEMS = [
    Item("Neeko", component_names=[], consumable=True, emblem=False),
    Item("Magnetic Remover", component_names=[], consumable=True, emblem=False),
    Item("Reforger", component_names=[], consumable=True, emblem=False)
  ]

  for item_data in items_data:
    components = item_data["components"] if "components" in item_data else []
    ALL_ITEMS.append(Item(
      name=item_data["name"],
      component_names=components,
      consumable=False,
      emblem="Spatula" in components
    ))

  for item in ALL_ITEMS:
    item.compile_components()

  json_file.close()