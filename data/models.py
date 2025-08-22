import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass(order=True, kw_only=True)
class Entity(ABC):
    """
    An abstract dataclass for any entity in the game.
    """

    name: str
    hp: int
    damage: int
    is_defending: bool = field(default=False)
    max_hp: int

    def is_alive(self) -> bool:
        return self.hp > 0

    @abstractmethod
    def take_damage(self, amount: int):
        pass

    @abstractmethod
    def attack(self, entity: "Entity"):
        pass


@dataclass
class Player(Entity):
    inventory: List[str] = field(default_factory=list, kw_only=True)

    def take_damage(self, amount: int):
        if self.is_defending:
            amount = round(amount / random.uniform(1.8, 2.5))

        final_damage = max(0, amount)
        self.hp = max(0, self.hp - final_damage)
        self.is_defending = False

    def attack(self, entity: Entity):
        attack_damage = random.randint(self.damage - 2, self.damage + 2)
        entity.take_damage(attack_damage)

    def has_item(self, item) -> bool:
        return item in self.inventory


@dataclass
class Enemy(Entity):
    def take_damage(self, amount: int):
        if self.is_defending:
            amount = round(amount / random.uniform(1.2, 1.8))

        final_damage = max(0, amount)
        self.hp = max(0, self.hp - final_damage)
        self.is_defending = False

    def attack(self, entity: Entity):
        attack_damage = random.randint(self.damage - 4, self.damage + 2)
        entity.take_damage(attack_damage)
