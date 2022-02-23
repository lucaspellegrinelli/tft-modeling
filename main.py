import matplotlib.pyplot as plt

from tft.game import TFTGame
from stupidplayer import StupidPlayer

players = [StupidPlayer() for _ in range(8)]
player_life = [[] for _ in players]
player_level = [[] for _ in players]
player_gold = [[] for _ in players]

def round_callback(game):
  global player_life
  for i, player in enumerate(game.players):
    player_life[i].append(player.health)
    player_level[i].append(player.level)
    player_gold[i].append(player.gold)

game = TFTGame(players)
game.run_game(round_callback)

all_players = game.players
for i, player in enumerate(all_players):
  print(f"Player {i}")
  print(f" * Reroll Level = {player.reroll_level}")
  # print(f" * Level = {player.level}")
  # print(f" * XP = {player.xp}")
  # print(f" * Gold = {player.gold}")
  # print(f" * Field = {player.units_in_play}")
  # print(f" * Bench = {player.units_in_bench}")
  # print(f" * Items = {player.items}")
  # print(f"")

fig, axs = plt.subplots(2, 2)


axs[0, 0].set_title("Level")
for i, p in enumerate(player_level):
  axs[0, 0].plot(p, label=f"Player {i}")

axs[0, 1].set_title("Gold")
for i, p in enumerate(player_gold):
  axs[0, 1].plot(p, label=f"Player {i}")

axs[1, 0].set_title("Health")
for i, p in enumerate(player_life):
  axs[1, 0].plot(p, label=f"Player {i}")

axs[0, 0].legend(loc="best")
axs[1, 0].legend(loc="best")
axs[0, 1].legend(loc="best")
plt.show()