from dataclasses import dataclass, field

from .constants import ArmourGroup, WeaponGroup
from .features import Reference


@dataclass
class Item:
    name: str
    description: str = ""
    quantity: int = 1
    reference: Reference | None = None


@dataclass(kw_only=True)
class Magic:
    rarity: str | None = None
    requires_attunement: bool = False


@dataclass
class Weapon(Item):
    damage: str = ""
    damage_type: str = ""
    properties: list[str] = field(default_factory=list)
    proficiency_group: WeaponGroup = "simple"


@dataclass
class MagicWeapon(Weapon, Magic):
    pass


@dataclass
class Armour(Item):
    base_ac: int = 10
    dexterity_cap: int | None = None
    stealth_disadvantage: bool = False
    proficiency_group: ArmourGroup = "light"


@dataclass
class MagicArmour(Armour, Magic):
    pass


@dataclass(kw_only=True)
class Tool(Item):
    proficiency_group: str


@dataclass
class MiscItem(Item):
    quantity: int = 1


@dataclass
class MagicMiscItem(MiscItem, Magic):
    pass

