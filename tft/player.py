from tft.items import Item
from tft.unit import Unit
from tft.tomes import Tome
from tft.drops import Drops

class Player:
  BENCH_SIZE = 10

  UPDATE_SHOP_COST = 2
  ROUND_BASE_GOLD_INCOME = 5
  PVP_WIN_GOLD_INCOME = 1
  STREAK_GOLD_BONUSES = lambda streak: streak - 2 if streak >= 3 else streak - 1
  INCOME_GOLD_BONUSES = lambda gold: min(gold, 50) // 10

  ROUND_BASE_XP_GAIN = 2
  BUY_XP_PRICE = 4
  BUY_XP_GAIN = 4
  XP_TO_LEVEL_UP = [0, 2, 6, 10, 20, 36, 56, 80, 100] # Level X
  MAX_LEVEL = 9

  def __init__(self):
    self.health = 100
    self.gold = 0
    self.xp = 0
    self.level = 1
    self.items = []
    self.units_in_play = []
    self.units_in_bench = []
    self.units_in_shop = []
    self.tomes = []

    self.last_pvp_results = []

  def play_round(self, game):
    raise NotImplementedError()

  def change_round(self):
    streak = self.get_streak()
    self.gold += Player.ROUND_BASE_GOLD_INCOME + Player.STREAK_GOLD_BONUSES(streak) + Player.INCOME_GOLD_BONUSES(self.gold)
    self.gain_xp(Player.ROUND_BASE_XP_GAIN)

  def pre_round(self):
    if len(self.units_in_bench) > 0 and len(self.units_in_play) < self.level:
      self.play_unit(self.units_in_bench[0])

  def give_drop(self, drop):
    assert(isinstance(drop, Drops))
    self.gold += drop.gold
    for item in drop.items: self.give_item(item)
    for unit in drop.units: self.give_unit(unit)
    for tome in drop.tomes: self.give_tome(tome)

  def give_unit(self, unit):
    assert(isinstance(unit, Unit))
    combine_bench_indexes, combine_field_indexes = self.would_combine_with(unit)

    if (len(combine_bench_indexes) + len(combine_field_indexes)) >= 2:
      if len(combine_field_indexes) > 0:
        old_unit_a = self.units_in_play.pop(combine_field_indexes[0])
        if len(combine_field_indexes) > 1:
          old_unit_b = self.units_in_play.pop(combine_field_indexes[1] - 1)
        else:
          old_unit_b = self.units_in_bench.pop(combine_bench_indexes[0])
      else:
        old_unit_a = self.units_in_bench.pop(combine_bench_indexes[0])
        old_unit_b = self.units_in_bench.pop(combine_bench_indexes[1] - 1)

      unit.stars += 1
      old_units_items = old_unit_a.items + old_unit_b.items
      for item in old_units_items:
        if unit.give_item(item):
          old_units_items.remove(item)
        else:
          self.items.append(item)

      if len(combine_field_indexes) > 0:
        self.units_in_play.append(unit)
      else:
        self.units_in_bench.append(unit)
    else:
      self.units_in_bench.append(unit)

  def give_item(self, item):
    assert(isinstance(item, Item))
    self.items.append(item)

  def give_tome(self, tome):
    assert(isinstance(tome, Tome))
    self.tomes.append(tome)

  def buy_xp(self):
    assert(self.gold >= Player.BUY_XP_PRICE)
    assert(self.level < Player.MAX_LEVEL)
    self.gold -= Player.BUY_XP_PRICE
    self.gain_xp(Player.BUY_XP_GAIN)

  def reset_shop(self, game, auto_refresh=False):
    if not auto_refresh:
      assert(self.gold >= Player.UPDATE_SHOP_COST)
      self.gold -= Player.UPDATE_SHOP_COST
    self.units_in_shop = game.get_new_shop(self.level)

  def buy_unit(self, unit):
    assert(isinstance(unit, Unit))
    assert(unit in self.units_in_shop)
    assert(self.gold >= unit.champion.cost)
    assert(len(self.units_in_bench) < Player.BENCH_SIZE)
    self.gold -= unit.champion.cost
    self.give_unit(unit)
    self.units_in_shop.remove(unit)

  def sell_unit(self, unit):
    assert(isinstance(unit, Unit))
    assert(unit in self.units_in_play or unit in self.units_in_bench)
    self.gold += unit.champion.cost * unit.stars - (unit.stars > 1)
    if unit in self.units_in_play: self.units_in_play.remove(unit)
    if unit in self.units_in_bench: self.units_in_bench.remove(unit)
    self.items += unit.items

  def play_unit(self, unit):
    assert(isinstance(unit, Unit))
    assert(unit in self.units_in_bench)
    assert(not self.is_field_full())
    self.units_in_play.append(unit)
    self.units_in_bench.remove(unit)

  def bench_unit(self, unit):
    assert(isinstance(unit, Unit))
    assert(unit in self.units_in_play)
    assert(not self.is_bench_full())
    self.units_in_bench.append(unit)
    self.units_in_play.remove(unit)

  def swap_unit(self, field_unit, bench_unit):
    assert(isinstance(field_unit, Unit))
    assert(isinstance(bench_unit, Unit))
    assert(field_unit in self.units_in_play)
    assert(bench_unit in self.units_in_bench)
    self.units_in_play.append(bench_unit)
    self.units_in_play.remove(field_unit)
    self.units_in_bench.append(field_unit)
    self.units_in_bench.remove(bench_unit)

  def use_item(self, item, unit):
    assert(isinstance(item, Item))
    assert(isinstance(unit, Unit))
    assert(unit in self.units_in_play or unit in self.units_in_bench)
    assert(item in self.items)

    def use_neeko(unit):
      if len(self.units_in_bench) >= Player.BENCH_SIZE: return False
      self.units_in_bench(Unit(unit.champion))
      return True

    def use_magnetic_remover(unit):
      if len(self.items) == 0: return False
      self.items += unit.items
      unit.items = []
      return True

    def use_reforger(unit):
      if len(self.items) == 0: return False
      new_items = []
      for item in unit.items:
        if item.is_simple():
          new_items.append(Item.get_random(count=1, simple_only=True))
        else:
          new_items.append(Item.get_random(count=1, composite_only=True))
      unit.items = []
      self.items += new_items
      return True

    if item.is_consumable():
      if item.name == "Neeko":
        return use_neeko(unit)
      elif item.name == "Magnetic Remover":
        return use_magnetic_remover(unit)
      elif item.name == "Reforger":
        return use_reforger(unit)
      else:
        return False
    else:
      return unit.give_item(item)

  def gain_xp(self, amount):
    if self.level < Player.MAX_LEVEL:
      self.xp += amount
    if self.xp >= Player.XP_TO_LEVEL_UP[self.level - 1]:
      self.xp -= Player.XP_TO_LEVEL_UP[self.level - 1]
      self.level += 1

  def get_streak(self):
    streak = 1
    for i in range(len(self.last_pvp_results) - 2, -1, -1):
      if self.last_pvp_results[i] == self.last_pvp_results[i + 1]:
        streak += 1
      else:
        break
    return streak

  def report_match_result(self, won):
    assert(not self.is_dead())
    self.last_pvp_results.append(won)

  def is_dead(self):
    return self.health <= 0

  def take_damage(self, damage):
    self.health = max(0, self.health - damage)

  def would_combine_with(self, unit):
    assert(isinstance(unit, Unit))
    combine_bench_indexes = []
    for i, bench_unit in enumerate(self.units_in_bench):
      if bench_unit.can_combine_with(unit):
        combine_bench_indexes.append(i)

    combine_field_indexes = []
    for i, field_unit in enumerate(self.units_in_play):
      if field_unit.can_combine_with(unit):
        combine_field_indexes.append(i)

    return combine_bench_indexes, combine_field_indexes

  def is_field_full(self):
    return len(self.units_in_play) >= self.level

  def is_bench_full(self):
    return len(self.units_in_bench) >= Player.BENCH_SIZE