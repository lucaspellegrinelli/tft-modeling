import random
from tft.player import Player

class StupidPlayer(Player):
  def __init__(self):
    super().__init__()
    self.reroll_level = random.randint(7, 9)
    self.critical_health = random.randint(20, 40)

  def find_worst_unit(self, where):
    worst_unit = None
    worst_score = 999999999999
    for unit in where:
      score = unit.champion.cost * unit.stars
      if score < worst_score:
        worst_score = score
        worst_unit = unit
    return worst_unit, worst_score

  def find_best_unit(self, where):
    best_unit = None
    best_score = 0
    for unit in where:
      score = unit.champion.cost * unit.stars
      if score > best_score:
        best_score = score
        best_unit = unit
    return best_unit, best_score

  def sell_bad_units(self):
    sold_something = False
    for i, unit_a in enumerate(self.units_in_bench + self.units_in_play):
      has_pair = False
      for j, unit_b in enumerate(self.units_in_bench + self.units_in_play):
        if i == j: continue
        if unit_a.can_combine_with(unit_b):
          has_pair = True
          break

      if has_pair:
        self.sell_unit(unit_a)
        sold_something = True
        break
    
    if not sold_something:
      worst_unit, _ = self.find_worst_unit(self.units_in_bench)
      self.sell_unit(worst_unit)

  def look_for_upgrades(self):
    for unit in self.units_in_shop:
      unit_score = unit.champion.cost * unit.stars
      a, b = self.would_combine_with(unit)
      if len(a) + len(b) >= 2:
        while self.is_bench_full():
          self.sell_bad_units()
        
        if self.gold >= unit.champion.cost:
          self.buy_unit(unit)
        continue
      else:
        worst_bench_unit, worst_bench_score = self.find_worst_unit(self.units_in_bench)
        if worst_bench_score < unit_score:
          self.sell_unit(worst_bench_unit)
          while self.is_bench_full():
            self.sell_bad_units()
          self.buy_unit(unit)

  def reorder_field(self):
    all_units = self.units_in_bench + self.units_in_play
    all_units = sorted(all_units, key=lambda unit: unit.champion.cost * unit.stars)

    while True:
      worst_field_unit, worst_field_score = self.find_worst_unit(self.units_in_play)
      best_bench_unit, best_bench_score = self.find_best_unit(self.units_in_bench)
      if best_bench_unit is None or worst_field_unit is None: break

      if len(self.units_in_play) < self.level:
        self.play_unit(best_bench_unit)
      elif best_bench_score > worst_field_score:
        self.swap_unit(worst_field_unit, best_bench_unit)
      else:
        break

  def play_round(self, game):
    self.look_for_upgrades()

    if self.health < self.critical_health:
      while self.gold > 5:
        self.reset_shop(game)
        self.look_for_upgrades()
    else:
      while self.level < self.reroll_level and self.gold >= 54:
        self.buy_xp()
        
      while self.level == self.reroll_level and self.gold >= 52:
        self.reset_shop(game)
        self.look_for_upgrades()

    self.reorder_field()