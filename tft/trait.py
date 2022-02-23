import json
import copy

ALL_TRAITS = []

class Trait:
  def __init__(self, name, levels):
    self.name = name
    self.states = levels

  def __repr__(self):
    return self.name

  @staticmethod
  def get_all():
    return copy.deepcopy(ALL_TRAITS)

  @staticmethod
  def from_name(name):
    for trait in ALL_TRAITS:
      if trait.name == name:
        return copy.deepcopy(trait)
    raise Exception(f"Could'nt find trait with name {name}")

# Loading data on load file
def initialize_traits():
  global ALL_TRAITS
  json_file = open("tft/data/traits.json", "r")
  traits_data = json.load(json_file)
  ALL_TRAITS = []
  for trait_data in traits_data:
    ALL_TRAITS.append(Trait(
      name=trait_data["name"],
      levels=trait_data["levels"]
    ))

  json_file.close()