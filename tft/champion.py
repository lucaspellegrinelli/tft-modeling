import json
import copy

ALL_CHAMPIONS = []

class Champion:
  def __init__(self, name, cost, traits):
    self.name = name
    self.cost = cost
    self.traits = traits

  def __repr__(self):
    return self.name

  def __eq__(self, other):
    return isinstance(other, Champion) and other.name == self.name

  @staticmethod
  def get_all():
    return copy.deepcopy(ALL_CHAMPIONS)

  @staticmethod
  def from_name(name):
    for champion in ALL_CHAMPIONS:
      if champion.name == name:
        return copy.deepcopy(champion)
    raise Exception(f"Could'nt find champion with name {name}")

# Loading data on load file
def initialize_champions():
  global ALL_CHAMPIONS
  json_file = open("tft/data/champions.json", "r")
  champions_data = json.load(json_file)

  for champion_data in champions_data:
    ALL_CHAMPIONS.append(Champion(
      name=champion_data["name"],
      cost=int(champion_data["cost"]),
      traits=champion_data["traits"]
    ))
  json_file.close()