class Tome:
  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return self.name

  @staticmethod
  def from_name(name):
    if name == "Tome of Emblem":
      return TomeOfEmblem()
    
    raise Exception(f"Could'nt find tome with name {name}")

class TomeOfEmblem(Tome):
  def __init__(self):
    super().__init__("Tome of Emblem")