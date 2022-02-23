class Drops:
  def __init__(self, gold=0, items=[], units=[], tomes=[]):
    self.gold = gold
    self.items = items
    self.units = units
    self.tomes = tomes

  def __repr__(self):
    repr_items = []
    if self.gold > 0:
      repr_items.append(f"Gold: {self.gold}")

    if len(list(filter(lambda item: item is not None, self.items))) > 0:
      repr_items.append(f"Items: {self.items}")

    if len(list(filter(lambda unit: unit is not None, self.units))) > 0:
      repr_items.append(f"Units: {self.units}")

    if len(list(filter(lambda tome: tome is not None, self.tomes))) > 0:
      repr_items.append(f"Tomes: {self.tomes}")

    return " | ".join(repr_items)

