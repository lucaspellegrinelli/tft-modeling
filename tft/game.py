import random

from tft.champion import Champion
from tft.unit import Unit
from tft.round import CarouselRound, DrakeRound, ElderOfHeraldRound, KrugsRound, PVPRound, FirstMinionRound, RaptorsRound, SecondMinionRound, ThirdMinionRound, WolvesRound

class TFTGame:
  UNITS_IN_SHOP = 5
  CHAMPION_POOL_SIZES = [29, 22, 18, 12, 10] # X stars
  REROLL_PROBABILITIES = [
    [1.00, 0.00, 0.00, 0.00, 0.00],
    [1.00, 0.00, 0.00, 0.00, 0.00],
    [0.75, 0.25, 0.00, 0.00, 0.00],
    [0.55, 0.30, 0.15, 0.00, 0.00],
    [0.45, 0.33, 0.20, 0.02, 0.00],
    [0.25, 0.40, 0.30, 0.05, 0.00],
    [0.19, 0.30, 0.35, 0.15, 0.01],
    [0.16, 0.20, 0.35, 0.25, 0.04],
    [0.09, 0.15, 0.30, 0.30, 0.16],
    [0.05, 0.10, 0.20, 0.40, 0.25],
  ]

  ROUNDS = [
    CarouselRound, FirstMinionRound, SecondMinionRound, ThirdMinionRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, KrugsRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, WolvesRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, RaptorsRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, DrakeRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, ElderOfHeraldRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, ElderOfHeraldRound,
    PVPRound, PVPRound, PVPRound, CarouselRound, PVPRound, PVPRound, ElderOfHeraldRound
  ]

  def __init__(self, players):
    self.turn = 0
    self.champions = Champion.get_all()
    self.champion_pool = { champion.name: TFTGame.CHAMPION_POOL_SIZES[champion.cost - 1] for champion in self.champions }
    self.players = players

  def run_game(self, round_callback=None):
    for round in TFTGame.ROUNDS:
      for player in self.players: player.pre_round()
      round().resolve(self)
      if round_callback is not None: round_callback(self)
      if self.game_ended(): break
      for player in self.players: player.change_round()
      self.turn += 1
      for player in self.players: player.play_round(self)

  def get_players_alive(self):
    return filter(lambda player: not player.is_dead(), self.players)

  def get_random_pooled_champions(self, count, costs=[1, 2, 3, 4, 5], remove_from_pool=True):
    eligible_champions = []
    for champion in self.champions:
      if champion.cost in costs:
        eligible_champions += [champion.name] * self.champion_pool[champion.name]

    chosen_champions = random.sample(eligible_champions, count)

    if remove_from_pool:
      for champion_name in chosen_champions:
        self.champion_pool[champion_name] -= 1

    return chosen_champions

  def get_new_shop(self, level):
    shop_units = []
    reroll_probs = TFTGame.REROLL_PROBABILITIES[level - 1]

    for _ in range(TFTGame.UNITS_IN_SHOP):
      target_star = random.choices([1, 2, 3, 4, 5], weights=reroll_probs, k=1)[0]
      rolled_champion = self.get_random_pooled_champions(1, costs=[target_star], remove_from_pool=False)[0]
      rolled_unit = Unit.from_name(rolled_champion)
      shop_units.append(rolled_unit)
    return shop_units

  def current_stage(self):
    if self.turn < 4:
      return 1
    else:
      return (self.turn - 4) // 7 + 2

  def game_ended(self):
    return len(list(self.get_players_alive())) <= 1