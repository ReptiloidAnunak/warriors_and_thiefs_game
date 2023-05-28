from __future__ import annotations
from abc import ABC, abstractmethod
from equipment import Equipment, Weapon, Armor
from classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = Equipment().get_weapon("ладошки")
        self.armor = Equipment().get_armor("футболка")
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor
        return f"{self.name} экипирован броней {self.weapon.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage = damage - target.armor.defence * target.unit_class.armor
        else:
            pass
        damage = target.get_damage(damage)
        return damage

    def get_damage(self, damage: int) -> Optional[int]:
        if damage > 0:
            self.hp -= damage
            self.hp = self.hp
            return round(damage, 1)
        return 0


    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        pass

    def use_skill(self, target: BaseUnit) -> str:
        if self._is_skill_used:
            return f"Навык {self.unit_class.skill.name} уже использован!"
        else:
            result = self.unit_class.skill().use(user=self, target=target)
            self._is_skill_used = True
            return result


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        Вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina <= self.weapon.stamina_per_hit * self.unit_class.stamina:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = round(self._count_damage(target), 1)
        if damage == 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """

        if not self._is_skill_used:
            if randint(1, 100) < 10:
               return self.use_skill(target)

        if self.stamina < 2:
            if randint(1, 10) < 3:
                # Регенерация выносливости игрока и противника эквивалентны STAMINA_PER_ROUND в base.Arena
                self.stamina += 1
                if target.stamina < target.unit_class.max_stamina:
                    target.stamina += 1
                return f"{self.name} пропустил ход, чтобы немного передохнуть"

        if self.stamina <= self.weapon.stamina_per_hit * self.unit_class.stamina:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."
        damage = round(self._count_damage(target), 1)
        if damage == 0:
            return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."
        else:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."




