# py/spells.py
from dataclasses import dataclass, field

from .constants import Ability, Preparation, PreparedSpellRule
from .features import Reference


@dataclass
class Spell:
    name: str
    level: int
    school: str | None = None
    ritual: bool = False
    description: str = ""
    reference: Reference | None = None


@dataclass
class SpellAccess:
    spell: Spell
    preparation: Preparation = "known"
    ability_override: Ability | None = None
    can_use_spell_slots: bool = True
    uses_per_rest: int | None = None


@dataclass
class SpellPool:
    name: str
    ability: Ability | None = None
    spells: list[SpellAccess] = field(default_factory=list)
    prepared_spell_rule: PreparedSpellRule | None = None

    def get_spells_by_level(self, level: int) -> list[SpellAccess]:
        return [sa for sa in self.spells if sa.spell.level == level]

