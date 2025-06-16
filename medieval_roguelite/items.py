import random

class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

# Predefined list of 10 items with simple effects
ITEMS = [
    Item("Healing Potion", "restore 1 health"),
    Item("Iron Sword", "increase attack"),
    Item("Wooden Shield", "reduce damage"),
    Item("Boots of Speed", "move faster"),
    Item("Magic Scroll", "random buff"),
    Item("Bomb", "damage enemies"),
    Item("Gold Coin", "increase score"),
    Item("Ring of Strength", "increase attack"),
    Item("Helmet", "reduce damage"),
    Item("Amulet of Power", "increase all stats"),
]

def random_item():
    """Return a random Item instance from the list."""
    return random.choice(ITEMS)
