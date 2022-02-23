from tft.champion import Champion
from tft.drops import Drops
from tft.items import Item
from tft.tomes import Tome
from tft.unit import Unit

class MultipleDropDescription:
  def __init__(self, drop_descriptions=[]):
    self.drop_descriptions = drop_descriptions

  def resolve(self, game):
    gold_drops = 0
    items_drops = []
    unit_drops = []
    tome_drops = []

    for drop_desc in self.drop_descriptions:
      if isinstance(drop_desc, GoldDropDescription):
        gold_drops += drop_desc.resolve(game)
      elif isinstance(drop_desc, ItemDropDescription):
        items_drops += drop_desc.resolve(game)
      elif isinstance(drop_desc, ChampionDropDescription) or isinstance(drop_desc, RandomChampionDropDescription):
        unit_drops += drop_desc.resolve(game)
      elif isinstance(drop_desc, TomeDropDescription):
        tome_drops += drop_desc.resolve(game)

    return Drops(gold_drops, items_drops, unit_drops, tome_drops)

class SingleDropDescription:
  def resolve(self, _):
    raise NotImplementedError()

class GoldDropDescription(SingleDropDescription):
  def __init__(self, amount):
    self.amount = amount

  def resolve(self, _):
    return self.amount

class ItemDropDescription(SingleDropDescription):
  def __init__(self, name, amount=1):
    self.name = name
    self.amount = amount

  def resolve(self, _):
    return [Item.from_name(self.name) for _ in range(self.amount)]

class ChampionDropDescription(SingleDropDescription):
  def __init__(self, name, amount=1):
    self.name = name
    self.amount = amount

  def resolve(self, _):
    return [Unit.from_name(self.name) for _ in range(self.amount)]

class RandomChampionDropDescription(SingleDropDescription):
  def __init__(self, costs, amount=1):
    self.costs = costs
    self.amount = amount

  def resolve(self, game):
    return list(map(Unit.from_name, game.get_random_pooled_champions(self.amount, costs=self.costs)))

class TomeDropDescription(SingleDropDescription):
  def __init__(self, name, amount=1):
    self.name = name
    self.amount = amount

  def resolve(self, _):
    return [Tome.from_name(self.name) for _ in range(self.amount)]