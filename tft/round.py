import random

from tft.battle import Battle
from tft.orbs import BlueOrb
from tft.items import Item
from tft.drops import Drops
from tft.unit import Unit

class Round:
  def resolve(self, game):
    raise NotImplementedError()

# Pvp Round
class PVPRound(Round):
  def resolve(self, game):
    players_alive = list(game.get_players_alive())
    player_indexes = list(range(len(players_alive)))
    player_pairs = []
    for _ in range(len(players_alive) // 2):
      a = random.choice(player_indexes)
      player_indexes.remove(a)
      b = random.choice(player_indexes)
      player_indexes.remove(b)
      player_pairs.append((a, b))

    for missed_idx in player_indexes:
      player = players_alive[missed_idx]
      player.report_match_result(True)

    for a_idx, b_idx in player_pairs:
      player_a = players_alive[a_idx]
      player_b = players_alive[b_idx]
      player_a_won, damage_dealt = Battle.player_battle(player_a, player_b, game.current_stage())
      player_a.report_match_result(player_a_won)
      player_b.report_match_result(not player_a_won)

      if player_a_won:
        player_b.take_damage(damage_dealt)
      else:
        player_a.take_damage(damage_dealt)

# Carousel Round
class CarouselRound(Round):
  def resolve(self, game):
    def create_carousel_unit(game):
      unit = Unit.from_name(game.get_random_pooled_champions(count=1, costs=[1, 2], remove_from_pool=False)[0])
      item = Item.get_random(count=1, simple_only=True)[0]
      unit.give_item(item)
      return unit

    for player in game.get_players_alive():
      unit = create_carousel_unit(game)
      player.give_unit(unit)

# NPC Rounds
class FirstMinionRound(Round):
  def resolve(self, game):
    def create_drop(game):
      return BlueOrb().get_drop(game)

    for player in game.get_players_alive():
      player.give_drop(create_drop(game))
    
class SecondMinionRound(Round):
  def resolve(self, game):
    def create_drop(game):
      return BlueOrb().get_drop(game)
      
    for player in game.get_players_alive():
      player.give_drop(create_drop(game))

class ThirdMinionRound(Round):
  def resolve(self, game):
    def create_drop(game):
      return BlueOrb().get_drop(game)
      
    for player in game.get_players_alive():
      player.give_drop(create_drop(game))

class KrugsRound(Round):
  def resolve(self, game):
    return BlueOrb().get_drop(game)

class WolvesRound(Round):
  def resolve(self, game):
    def create_drop(game):
      return BlueOrb().get_drop(game)
      
    for player in game.get_players_alive():
      player.give_drop(create_drop(game))

class RaptorsRound(Round):
  def resolve(self, game):
    def create_drop(game):
      return BlueOrb().get_drop(game)
      
    for player in game.get_players_alive():
      player.give_drop(create_drop(game))

class DrakeRound(Round):
  def resolve(self, game):
    def create_drop():
      item = Item.get_random(count=1, composite_only=True)[0]
      return Drops(items=[item])
    
    for player in game.get_players_alive():
      player.give_drop(create_drop())

class ElderOfHeraldRound(Round):
  def resolve(self, game):
    def create_drop():
      item = Item.get_random(count=1, composite_only=True)[0]
      return Drops(items=[item])
    
    for player in game.get_players_alive():
      player.give_drop(create_drop())