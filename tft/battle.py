import random

class Battle:
  DAMAGE_FROM_UNITS = [2, 4, 6, 8, 10, 11, 12, 13, 14, 15] # X units left in the opponent field
  DAMAGE_FROM_STAGE = [0, 0, 2, 3, 5, 8, 15] # X stage

  @staticmethod
  def player_battle(player_a, player_b, stage):
    def calculate_unit_scores(unit):
      return unit.champion.cost * unit.stars + len(unit.items)

    def unit_battle(a, b):
      f = (b / a)**(0.5)
      return f * random.uniform(0, 1) <= 0.5

    a_scores = [calculate_unit_scores(unit) for unit in player_a.units_in_play]
    b_scores = [calculate_unit_scores(unit) for unit in player_b.units_in_play]

    while len(a_scores) > 0 and len(b_scores) > 0:
      a_unit = random.choice(a_scores)
      b_unit = random.choice(b_scores)
      a_unit_won = unit_battle(a_unit, b_unit)
      if a_unit_won:
        b_scores.remove(b_unit)
      else:
        a_scores.remove(a_unit)

    player_a_won = len(a_scores) > 0
    units_left = len(a_scores) if player_a_won else len(b_scores)

    damage_dealt = Battle.DAMAGE_FROM_STAGE[stage - 1] + Battle.DAMAGE_FROM_UNITS[units_left - 1]
    return player_a_won, damage_dealt