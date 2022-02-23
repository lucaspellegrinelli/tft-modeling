from tft.game import TFTGame
from tft.unit import Unit

from stupidplayer import StupidPlayer

players = [StupidPlayer() for _ in range(8)]
game = TFTGame(players)
game.run_game()

all_players = game.players
for i, player in enumerate(all_players):
  print(f"Player {i}")
  print(f" * Health = {player.health}")
  print(f" * Level = {player.level}")
  print(f" * XP = {player.xp}")
  print(f" * Gold = {player.gold}")
  print(f" * Field = {player.units_in_play}")
  print(f" * Bench = {player.units_in_bench}")
  print(f" * Items = {player.items}")
  print(f"")