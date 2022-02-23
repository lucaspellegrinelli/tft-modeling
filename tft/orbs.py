import random

from tft.dropdescription import MultipleDropDescription
from tft.dropdescription import ItemDropDescription
from tft.dropdescription import GoldDropDescription
from tft.dropdescription import RandomChampionDropDescription
from tft.dropdescription import TomeDropDescription

class Orb:
  def __init__(self, possible_drops):
    probs, drops = zip(*possible_drops)
    assert(sum(probs) == 1)
    self.chosen_drop = random.choices(drops, weights=probs, k=1)[0]

  def get_drop(self, game):
    return self.chosen_drop.resolve(game)

  def __repr__(self):
    return str(self.drop)

class GrayOrb(Orb):
  def __init__(self):
    super().__init__([
      (0.10, MultipleDropDescription([GoldDropDescription(3)])),
      (0.22, MultipleDropDescription([GoldDropDescription(3), RandomChampionDropDescription(costs=[1])])),
      (0.22, MultipleDropDescription([GoldDropDescription(3), RandomChampionDropDescription(costs=[2])])),
      (0.02, MultipleDropDescription([GoldDropDescription(3), ItemDropDescription("Reforger")])),
      (0.02, MultipleDropDescription([GoldDropDescription(3), ItemDropDescription("Magnetic Remover")])),
      (0.40, MultipleDropDescription([RandomChampionDropDescription(costs=[3], amount=1)])),
      (0.02, MultipleDropDescription([ItemDropDescription("Neeko")]))
    ])

class BlueOrb(Orb):
  def __init__(self):
    super().__init__([
      (0.02, MultipleDropDescription([GoldDropDescription(5)])),
      (0.04, MultipleDropDescription([GoldDropDescription(6)])),
      (0.02, MultipleDropDescription([GoldDropDescription(5), ItemDropDescription("Magnetic Remover")])),
      (0.30, MultipleDropDescription([RandomChampionDropDescription(costs=[2], amount=3)])),
      (0.04, MultipleDropDescription([GoldDropDescription(5), ItemDropDescription("Reforger")])),
      (0.28, MultipleDropDescription([RandomChampionDropDescription(costs=[3], amount=2)])),
      (0.25, MultipleDropDescription([RandomChampionDropDescription(costs=[3], amount=1), RandomChampionDropDescription(costs=[2], amount=1)])),
      (0.01, MultipleDropDescription([ItemDropDescription("Neeko"), RandomChampionDropDescription(costs=[3])])),
      (0.04, MultipleDropDescription([GoldDropDescription(1), ItemDropDescription("Neeko"), RandomChampionDropDescription(costs=[2])]))
    ])

class GoldOrb(Orb):
  def __init__(self):
    super().__init__([
      (0.15, MultipleDropDescription([GoldDropDescription(10)])),
      (0.20, MultipleDropDescription([ItemDropDescription("Spatula")])),
      (0.15, MultipleDropDescription([GoldDropDescription(5), ItemDropDescription("Neeko")])),
      (0.20, MultipleDropDescription([TomeDropDescription("Tome of Emblem")])),
      (0.15, MultipleDropDescription([RandomChampionDropDescription(costs=[4], amount=2)])),
      (0.15, MultipleDropDescription([RandomChampionDropDescription(costs=[3], amount=3)])),
    ])