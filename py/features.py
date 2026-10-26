from dataclasses import dataclass

from .constants import (
    Ability,
    ArmourGroup,
    MovementType,
    SkillName,
    WeaponGroup,
    SKILL_ABILITIES,
)


@dataclass
class Reference:
    source: str = "PHB"
    page: int | None = None
    url: str | None = None

    def to_string(self) -> str:
        if self.url:
            return f"({self.url})"
        if self.page is not None:
            return f"({self.source} p.{self.page})"
        return f"({self.source})"


@dataclass
class Feature:
    name: str
    description: str = ""
    reference: Reference | None = None
    is_combat: bool = False


@dataclass
class CasterLevel:
    amount: float = 0
    description: str = ""
    reference: Reference | None = None


@dataclass
class Skill:
    name: SkillName
    proficient: bool = True
    expertise: bool = False
    description: str = ""
    reference: Reference | None = None

    @property
    def ability(self) -> Ability:
        return SKILL_ABILITIES[self.name]


@dataclass
class SavingThrow:
    name: Ability
    proficient: bool = True
    description: str = ""
    reference: Reference | None = None


@dataclass
class WeaponProficiency:
    name: WeaponGroup
    description: str = ""
    reference: Reference | None = None


@dataclass
class ArmourProficiency:
    name: ArmourGroup
    description: str = ""
    reference: Reference | None = None


@dataclass
class ToolProficiency:
    name: str
    description: str = ""
    reference: Reference | None = None


@dataclass
class LanguageProficiency:
    name: str
    description: str = ""
    reference: Reference | None = None


@dataclass
class AbilityScore:
    name: Ability
    amount: int = 0
    description: str = ""
    reference: Reference | None = None


@dataclass
class HitPoints:
    amount: int = 0
    description: str = ""
    reference: Reference | None = None


@dataclass
class InitiativeProficiency:
    proficient: bool = True
    description: str = ""
    reference: Reference | None = None


@dataclass
class Initiative:
    amount: float = 0
    description: str = ""
    reference: Reference | None = None


@dataclass
class Size:
    size: str
    description: str = ""
    reference: Reference | None = None


@dataclass
class Speed:
    amount: int = 30
    movement_type: MovementType = "walking"
    description: str = ""
    reference: Reference | None = None


CharacterFeature = (
    Feature
    | CasterLevel
    | Skill
    | SavingThrow
    | WeaponProficiency
    | ArmourProficiency
    | ToolProficiency
    | LanguageProficiency
    | AbilityScore
    | HitPoints
    | Initiative
    | InitiativeProficiency
    | Size
    | Speed
)

