# py/models.py
from dataclasses import dataclass, field

from .constants import Class
from .features import CharacterFeature, Reference
from .items import Item
from .spells import SpellPool


@dataclass
class Source:
    name: str
    reference: Reference | None = None
    features: list[CharacterFeature | list[CharacterFeature]] = field(
        default_factory=list
    )
    sources: list["Source"] = field(default_factory=list)
    spell_pools: list[SpellPool] = field(default_factory=list)


@dataclass
class ClassLevel:
    name: Class
    level: int
    hit_die: int
    hp_roll: int
    reference: Reference | None = None
    subclass: Source | None = None
    features: list[CharacterFeature | list[CharacterFeature]] = field(
        default_factory=list
    )
    sources: list[Source] = field(default_factory=list)
    spell_pools: list[SpellPool] = field(default_factory=list)

