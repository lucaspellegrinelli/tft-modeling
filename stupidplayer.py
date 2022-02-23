from tft.player import Player

class StupidPlayer(Player):
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
      worst_bench_unit = None
      worst_bench_score = 999999999999
      for bench_unit in self.units_in_bench:
        score = bench_unit.champion.cost * bench_unit.stars
        if score < worst_bench_score:
          worst_bench_score = score
          worst_bench_unit = bench_unit
      self.sell_unit(worst_bench_unit)

  def look_for_upgrades(self):
    for unit in self.units_in_shop:
      unit_score = unit.champion.cost * unit.stars
      a, b = self.would_combine_with(unit)
      if len(a) + len(b) >= 2:
        while self.is_bench_full():
          self.sell_bad_units()
        
        self.buy_unit(unit)
        continue

      worst_bench_unit = None
      worst_bench_score = 999999999999
      for bench_unit in self.units_in_bench:
        score = bench_unit.champion.cost * bench_unit.stars
        if score < worst_bench_score:
          worst_bench_score = score
          worst_bench_unit = bench_unit

      if worst_bench_score < unit_score:
        self.sell_unit(worst_bench_unit)
        while self.is_bench_full():
          self.sell_bad_units()
        self.buy_unit(unit)


  def reorder_field(self):
    all_units = self.units_in_bench + self.units_in_play
    all_units = sorted(all_units, key=lambda unit: unit.champion.cost * unit.stars)

    while True:
      worst_field_unit = None
      worst_field_score = 999999999999
      for unit in self.units_in_play:
        score = unit.champion.cost * unit.stars
        if score < worst_field_score:
          worst_field_score = score
          worst_field_unit = unit

      best_bench_unit = None
      best_bench_score = 0
      for unit in self.units_in_bench:
        score = unit.champion.cost * unit.stars
        if score > best_bench_score:
          best_bench_score = score
          best_bench_unit = unit

      if best_bench_unit is None or worst_field_unit is None:
        break

      if len(self.units_in_play) < self.level:
        self.play_unit(best_bench_unit)
      elif best_bench_score > worst_field_score:
        self.swap_unit(worst_field_unit, best_bench_unit)
      else:
        break

  def play_round(self, game):
    self.look_for_upgrades()
    while self.gold >= 52:
      self.reset_shop(game)
      self.look_for_upgrades()

    self.reorder_field()

    if self.level < Player.MAX_LEVEL:
      self.buy_xp()