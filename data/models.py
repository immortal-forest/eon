import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

# a dataclass basically does all the work for you
# like writing init funtion and other dunder methods (funtions like __str__, __repr__, etc)
# order preserves the order in which variables are declared
# kw_only makes it accept keywords args only, eg: function(arg1=value, arg2=value,...)

# ABC, tells python its an abstract class


@dataclass(order=True, kw_only=True)
class Entity(ABC):
    """
    An abstract dataclass for any entity in the game.
    """

    name: str
    hp: int
    damage: int
    # its how we declare default values for dataclass
    is_defending: bool = field(default=False)
    max_hp: int

    def is_alive(self) -> bool:
        return self.hp > 0

    @abstractmethod
    def take_damage(self, amount: int):
        pass

    @abstractmethod
    def attack(
        self, entity: "Entity"
    ):  # "Entity" for type hints, since the class isn't made yet
        pass


@dataclass
class Player(Entity):
    inventory: List[str] = field(default_factory=list, kw_only=True)

    def take_damage(self, amount: int):
        if self.is_defending:
            # Player's defense is stronger, reducing damage by 45% to 60%
            amount = round(amount / random.uniform(1.8, 2.5))

        final_damage = max(0, amount)
        self.hp = max(0, self.hp - final_damage)
        self.is_defending = False  # we defend once every turn

    def attack(self, entity: Entity):
        # varying by +/- 2 from base damage.
        attack_damage = random.randint(self.damage - 2, self.damage + 2)
        entity.take_damage(attack_damage)

    def has_item(self, item) -> bool:
        return item in self.inventory

    def has_items(self) -> bool:
        return bool(self.inventory)


@dataclass
class Enemy(Entity):
    def take_damage(self, amount: int):
        if self.is_defending:
            # Enemy's defense is weaker, reducing damage by 17% to 45%.
            amount = round(amount / random.uniform(1.2, 1.8))

        final_damage = max(0, amount)
        self.hp = max(0, self.hp - final_damage)
        self.is_defending = False

    def attack(self, entity: Entity):
        # Enemy's attack is more unpredictable than the player's.
        # -4 to +2 from base damage
        attack_damage = random.randint(self.damage - 4, self.damage + 2)
        entity.take_damage(attack_damage)

    def action(self, target: Entity):
        # Enemy's logic, 30% chance of defending
        if random.random() < 0.3:
            self.is_defending = True
        else:
            self.attack(target)
