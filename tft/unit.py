from tft.champion import Champion
from tft.items import Item

class Unit:
  MAX_ITEMS = 3

  def __init__(self, champion, stars=1, items=[]):
    self.champion = champion
    self.stars = stars
    self.items = items

  def give_item(self, item):
    assert(isinstance(item, Item))
    
    if item.is_composite():
      if len(self.items) < Unit.MAX_ITEMS:
        self.items.append(item)
        return True
    else:
      if self.has_simple_item():
        simple_item = list(filter(lambda item: item.is_simple(), self.items))[0]
        composite_item = Item.get_composition(simple_item, item)
        self.items.remove(simple_item)
        self.items.append(composite_item)
        return True
      elif len(self.items) < Unit.MAX_ITEMS:
        self.items.append(item)
        return True
    return False

  def has_simple_item(self):
    return any([item.is_simple() for item in self.items])

  def can_combine_with(self, other):
    assert(isinstance(other, Unit))
    return self.champion.name == other.champion.name and self.stars == other.stars and other.stars <= 2

  def __eq__(self, other):
    a = isinstance(other, Unit)
    b = self.champion == other.champion
    c = self.stars == other.stars
    d = self.items == other.items
    return a and b and c and d

  def __repr__(self):
    return f"{self.stars}* {self.champion.name} {self.items}"

  @staticmethod
  def from_name(name):
    return Unit(Champion.from_name(name), stars=1, items=[])