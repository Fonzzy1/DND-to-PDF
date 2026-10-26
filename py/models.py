from dataclasses import dataclass, field
from typing import Literal
from warnings import warn
import math

# ============================================================
# TYPES AND RULE DEFINITIONS
# ============================================================

ordinal_dict = {
    1: "First",
    2: "Second",
    3: "Third",
    4: "Fourth",
    5: "Fifth",
    6: "Sixth",
    7: "Seventh",
    8: "Eighth",
    9: "Ninth",
}

WIZARD_PREPARED_SPELLS = {
    1: 4,
    2: 5,
    3: 6,
    4: 7,
    5: 9,
    6: 10,
    7: 11,
    8: 12,
    9: 14,
    10: 15,
    11: 16,
    12: 16,
    13: 17,
    14: 18,
    15: 19,
    16: 21,
    17: 22,
    18: 23,
    19: 24,
    20: 25,
}


MULTICLASS_SPELL_SLOTS = {
    1: (2, 0, 0, 0, 0, 0, 0, 0, 0),
    2: (3, 0, 0, 0, 0, 0, 0, 0, 0),
    3: (4, 2, 0, 0, 0, 0, 0, 0, 0),
    4: (4, 3, 0, 0, 0, 0, 0, 0, 0),
    5: (4, 3, 2, 0, 0, 0, 0, 0, 0),
    6: (4, 3, 3, 0, 0, 0, 0, 0, 0),
    7: (4, 3, 3, 1, 0, 0, 0, 0, 0),
    8: (4, 3, 3, 2, 0, 0, 0, 0, 0),
    9: (4, 3, 3, 3, 1, 0, 0, 0, 0),
    10: (4, 3, 3, 3, 2, 0, 0, 0, 0),
    11: (4, 3, 3, 3, 2, 1, 0, 0, 0),
    12: (4, 3, 3, 3, 2, 1, 0, 0, 0),
    13: (4, 3, 3, 3, 2, 1, 1, 0, 0),
    14: (4, 3, 3, 3, 2, 1, 1, 0, 0),
    15: (4, 3, 3, 3, 2, 1, 1, 1, 0),
    16: (4, 3, 3, 3, 2, 1, 1, 1, 0),
    17: (4, 3, 3, 3, 2, 1, 1, 1, 1),
    18: (4, 3, 3, 3, 3, 1, 1, 1, 1),
    19: (4, 3, 3, 3, 3, 2, 1, 1, 1),
    20: (4, 3, 3, 3, 3, 2, 2, 1, 1),
}

Class = Literal[
    "Barbarian",
    "Bard",
    "Cleric",
    "Druid",
    "Fighter",
    "Monk",
    "Paladin",
    "Ranger",
    "Rogue",
    "Sorcerer",
    "Warlock",
    "Wizard",
]

PreparedSpellRule = Literal[
    "class_level_plus_ability_modifier",
    "half_class_level_plus_ability_modifier",
    "ability_modifier",
    "wizard_table",
    "all",
]

Ability = Literal[
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
]

SkillName = Literal[
    "acrobatics",
    "animal_handling",
    "arcana",
    "athletics",
    "deception",
    "history",
    "insight",
    "intimidation",
    "investigation",
    "medicine",
    "nature",
    "perception",
    "performance",
    "persuasion",
    "religion",
    "sleight_of_hand",
    "stealth",
    "survival",
]

WeaponGroup = Literal["simple", "martial"]
ArmourGroup = Literal["light", "medium", "heavy", "shields"]
Preparation = Literal["known", "always_prepared", "innate"]

MovementType = Literal[
    "walking",
    "flying",
    "swimming",
    "climbing",
    "burrowing",
]

SKILL_ABILITIES: dict[SkillName, Ability] = {
    "acrobatics": "dexterity",
    "animal_handling": "wisdom",
    "arcana": "intelligence",
    "athletics": "strength",
    "deception": "charisma",
    "history": "intelligence",
    "insight": "wisdom",
    "intimidation": "charisma",
    "investigation": "intelligence",
    "medicine": "wisdom",
    "nature": "intelligence",
    "perception": "wisdom",
    "performance": "charisma",
    "persuasion": "charisma",
    "religion": "intelligence",
    "sleight_of_hand": "dexterity",
    "stealth": "dexterity",
    "survival": "wisdom",
}


# ============================================================
# REFERENCES
# ============================================================


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


# ============================================================
# NAMED FEATURES
# ============================================================


@dataclass
class Feature:
    """A named feature, trait, or special ability."""

    name: str
    description: str = ""
    reference: Reference | None = None
    is_combat: bool = False


# ============================================================
# TYPED CHARACTER DATA
#
# These are deliberately independent of Feature.
# They describe structured data rather than named traits.
# ============================================================


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
    """A movement speed, defaulting to walking."""

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

# ============================================================
# SPELLS AND SPELL POOLS
# ============================================================


@dataclass
class Spell:
    """A spell definition, independent of character access."""

    name: str
    level: int
    school: str | None = None
    ritual: bool = False
    description: str = ""
    reference: Reference | None = None


@dataclass
class SpellAccess:
    """A way the character can access a spell."""

    spell: Spell
    preparation: Preparation = "known"
    ability_override: Ability | None = None
    can_use_spell_slots: bool = True
    uses_per_rest: int | None = None


@dataclass
class SpellPool:
    """Spells granted by a class, feat, race, subclass, or item."""

    name: str
    ability: Ability | None = None
    spells: list[SpellAccess] = field(default_factory=list)
    prepared_spell_rule: PreparedSpellRule | None = None

    def get_spells_by_level(self, level: int) -> list[SpellAccess]:
        return [sa for sa in self.spells if sa.spell.level == level]


# ============================================================
# ITEMS
# ============================================================


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


# ============================================================
# SOURCES AND CLASS LEVELS
# ============================================================


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


# ============================================================
# CHARACTER
# ============================================================


@dataclass
class Character:
    name: str

    abilities: dict[Ability, int] = field(
        default_factory=lambda: {
            "strength": 10,
            "dexterity": 10,
            "constitution": 10,
            "intelligence": 10,
            "wisdom": 10,
            "charisma": 10,
        }
    )

    race: Source | None = None
    background: Source | None = None
    classes: list[ClassLevel] = field(default_factory=list)

    items: list[Item] = field(default_factory=list)
    features: list[CharacterFeature] = field(default_factory=list)
    spell_pools: list[SpellPool] = field(default_factory=list)

    personality: str = ""
    ideals: str = ""
    bonds: str = ""
    flaws: str = ""

    def get_initiative_modifier(self) -> int:
        """Calculate initiative, including Dexterity and proficiency."""

        modifier = self.get_ability_modifier("dexterity")

        has_proficiency = any(
            feature
            for feature in self.get_features()
            if isinstance(feature, InitiativeProficiency)
        )
        if has_proficiency:
            modifier += self.get_proficiency_bonus()

        modifier += sum(
            feature.amount
            for feature in self.get_features()
            if isinstance(feature, Initiative)
        )

        return modifier

    # --------------------------------------------------------
    # LEVEL AND PROFICIENCY BONUS
    # --------------------------------------------------------

    def get_level(self) -> int:
        """Total character level, supporting cumulative class records."""

        class_levels: dict[str, int] = {}

        for cls in self.classes:
            class_levels[cls.name] = max(
                class_levels.get(cls.name, 0),
                cls.level,
            )

        return sum(class_levels.values())

    def get_class_level(self, class_name: Class) -> int:
        """Highest recorded level in a particular class."""

        return max(
            (cls.level for cls in self.classes if cls.name == class_name),
            default=0,
        )

    def get_proficiency_bonus(self) -> int:
        return 2 + max(0, self.get_level() - 1) // 4

    # --------------------------------------------------------
    # FEATURE COLLECTION
    # --------------------------------------------------------

    def get_features(self) -> list[CharacterFeature]:
        """Collect named features and typed character data."""

        result: list[CharacterFeature] = list(self.features)

        def add_contributions(
            contributions: list[CharacterFeature | list[CharacterFeature]],
        ) -> None:
            for contribution in contributions:
                if isinstance(contribution, list):
                    result.extend(contribution)
                else:
                    result.append(contribution)

        def collect(source: Source) -> None:
            add_contributions(source.features)

            for child in source.sources:
                collect(child)

        if self.race:
            collect(self.race)

        if self.background:
            collect(self.background)

        for cls in self.classes:
            add_contributions(cls.features)

            for source in cls.sources:
                collect(source)

            if cls.subclass:
                collect(cls.subclass)

        return result

    # --------------------------------------------------------
    # SPELL POOL COLLECTION
    # --------------------------------------------------------

    def get_spell_pools(self) -> dict[str, SpellPool]:
        """Aggregate pools by name across all character sources."""

        pools: dict[str, SpellPool] = {}

        def add_pool(contribution: SpellPool) -> None:
            pool = pools.get(contribution.name)

            if pool is None:
                pools[contribution.name] = SpellPool(
                    name=contribution.name,
                    ability=contribution.ability,
                    spells=list(contribution.spells),
                    prepared_spell_rule=contribution.prepared_spell_rule,
                )
                return

            if pool.ability != contribution.ability:
                raise ValueError(
                    f"Inconsistent spellcasting abilities for pool "
                    f"{contribution.name!r}"
                )

            existing_rule = pool.prepared_spell_rule
            incoming_rule = contribution.prepared_spell_rule

            if (
                existing_rule is not None
                and incoming_rule is not None
                and existing_rule != incoming_rule
            ):
                raise ValueError(
                    f"Inconsistent preparation rules for pool "
                    f"{contribution.name!r}"
                )

            if existing_rule is None:
                pool.prepared_spell_rule = incoming_rule

            pool.spells.extend(contribution.spells)

        def collect(source: Source) -> None:
            for pool in source.spell_pools:
                add_pool(pool)

            for child in source.sources:
                collect(child)

        for pool in self.spell_pools:
            add_pool(pool)

        if self.race:
            collect(self.race)

        if self.background:
            collect(self.background)

        for cls in self.classes:
            for pool in cls.spell_pools:
                add_pool(pool)

            for source in cls.sources:
                collect(source)

            if cls.subclass:
                collect(cls.subclass)

        for pool in pools.values():
            unique: dict[tuple, SpellAccess] = {}

            for access in pool.spells:
                key = (
                    access.spell.name,
                    access.preparation,
                    access.ability_override,
                    access.can_use_spell_slots,
                    access.uses_per_rest,
                )
                unique.setdefault(key, access)

            pool.spells = list(unique.values())

        return pools

    def get_spell_entries(self) -> list[tuple[str, SpellAccess]]:
        return [
            (pool.name, access)
            for pool in self.get_spell_pools().values()
            for access in pool.spells
        ]

    def get_spell_attack_bonus(self, ability: str) -> int:
        return self.get_proficiency_bonus() + self.get_ability_modifier(ability)

    def get_spell_save_dc(self, pool_name: str) -> int:
        return 8 + self.get_spell_attack_bonus(pool_name)

    def get_spells(self) -> list[Spell]:
        """Return unique spell definitions accessible to the character."""

        spells: dict[str, Spell] = {}

        for _, access in self.get_spell_entries():
            spells.setdefault(access.spell.name, access.spell)

        return list(spells.values())

    # --------------------------------------------------------
    # ABILITY SCORES
    # --------------------------------------------------------

    def get_ability_score(self, ability: Ability) -> int:
        base = self.abilities[ability]

        bonuses = sum(
            feature.amount
            for feature in self.get_features()
            if isinstance(feature, AbilityScore) and feature.name == ability
        )

        return base + bonuses

    def get_ability_modifier(self, ability: Ability) -> int:
        return (self.get_ability_score(ability) - 10) // 2

    # --------------------------------------------------------
    # HIT POINTS
    # --------------------------------------------------------

    def get_max_hp(self) -> int:
        con_modifier = self.get_ability_modifier("constitution")

        total = sum(cls.hp_roll + con_modifier for cls in self.classes)

        total += sum(
            feature.amount
            for feature in self.get_features()
            if isinstance(feature, HitPoints)
        )

        return total

    # --------------------------------------------------------
    # DUPLICATE PROFICIENCY HANDLING
    # --------------------------------------------------------

    def _unique_features(
        self,
        feature_type: type,
        key_func,
        merge_func=None,
    ) -> list:
        unique: dict[object, object] = {}

        for feature in self.get_features():
            if not isinstance(feature, feature_type):
                continue

            key = key_func(feature)

            if key in unique:
                warn(
                    f"Duplicate {feature_type.__name__}: {key!r}. "
                    "The additional proficiency may be wasted.",
                    stacklevel=2,
                )

                if merge_func:
                    unique[key] = merge_func(unique[key], feature)
            else:
                unique[key] = feature

        return list(unique.values())

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    def get_skills(self) -> list[Skill]:
        def merge(a: Skill, b: Skill) -> Skill:
            return Skill(
                name=a.name,
                proficient=a.proficient or b.proficient,
                expertise=a.expertise or b.expertise,
                description=a.description or b.description,
                reference=a.reference or b.reference,
            )

        return self._unique_features(
            Skill,
            key_func=lambda skill: skill.name,
            merge_func=merge,
        )

    def get_skill_modifier(self, name: SkillName) -> int:
        skills = [skill for skill in self.get_skills() if skill.name == name]

        modifier = self.get_ability_modifier(SKILL_ABILITIES[name])

        if not skills:
            return modifier

        skill = skills[0]

        if skill.proficient:
            multiplier = 2 if skill.expertise else 1
            modifier += self.get_proficiency_bonus() * multiplier

        return modifier

    # --------------------------------------------------------
    # SAVING THROWS
    # --------------------------------------------------------

    def get_saving_throws(self) -> list[SavingThrow]:
        def merge(a: SavingThrow, b: SavingThrow) -> SavingThrow:
            return SavingThrow(
                name=a.name,
                proficient=a.proficient or b.proficient,
                description=a.description or b.description,
                reference=a.reference or b.reference,
            )

        return self._unique_features(
            SavingThrow,
            key_func=lambda saving_throw: saving_throw.name,
            merge_func=merge,
        )

    def get_saving_throw_modifier(self, ability: Ability) -> int:
        modifier = self.get_ability_modifier(ability)

        proficient = any(
            saving_throw.name == ability and saving_throw.proficient
            for saving_throw in self.get_saving_throws()
        )

        if proficient:
            modifier += self.get_proficiency_bonus()

        return modifier

    # --------------------------------------------------------
    # PROFICIENCIES
    # --------------------------------------------------------

    def get_weapon_proficiencies(self) -> list[WeaponProficiency]:
        return self._unique_features(
            WeaponProficiency,
            key_func=lambda proficiency: proficiency.name,
        )

    def get_armour_proficiencies(self) -> list[ArmourProficiency]:
        return self._unique_features(
            ArmourProficiency,
            key_func=lambda proficiency: proficiency.name,
        )

    def get_tool_proficiencies(self) -> list[ToolProficiency]:
        return self._unique_features(
            ToolProficiency,
            key_func=lambda proficiency: proficiency.name.casefold(),
        )

    def get_languages(self) -> list[LanguageProficiency]:
        return self._unique_features(
            LanguageProficiency,
            key_func=lambda proficiency: proficiency.name.casefold(),
        )

    # --------------------------------------------------------
    # ITEM PROFICIENCY CHECK
    # --------------------------------------------------------
    def get_weapon_ability_modifier(self, weapon: Weapon) -> int:
        """Return the ability modifier used for a weapon attack."""

        properties = {prop.casefold() for prop in weapon.properties}

        if "finesse" in properties:
            return max(
                self.get_ability_modifier("strength"),
                self.get_ability_modifier("dexterity"),
            )

        return self.get_ability_modifier("strength")

    def get_weapon_attack_bonus(self, weapon: Weapon) -> int:
        """Calculate weapon attack bonus, including proficiency."""

        bonus = self.get_weapon_ability_modifier(weapon)

        if self.check_proficiency(weapon):
            bonus += self.get_proficiency_bonus()

        return bonus

    def get_weapon_damage(self, weapon: Weapon) -> str:
        """Return weapon damage dice plus its ability modifier."""

        modifier = self.get_weapon_ability_modifier(weapon)
        damage = weapon.damage

        if modifier:
            damage += f"{modifier:+d}"

        if weapon.damage_type:
            damage += f" {weapon.damage_type}"

        return damage

    def get_armour_class(self, armour: Armour | None = None) -> int:
        """Calculate AC for worn armour, or for an unarmoured character."""

        dex_modifier = self.get_ability_modifier("dexterity")

        if armour is None:
            return 10 + dex_modifier

        if armour.proficiency_group == "shields":
            return 10 + dex_modifier + armour.base_ac

        if armour.dexterity_cap is not None:
            dex_modifier = min(dex_modifier, armour.dexterity_cap)

        if armour.proficiency_group == "heavy":
            dex_modifier = 0

        return armour.base_ac + dex_modifier

    def check_proficiency(self, item: Item) -> bool:
        if isinstance(item, Weapon):
            proficiencies = {p.name for p in self.get_weapon_proficiencies()}

            if item.proficiency_group == "simple":
                return bool(proficiencies & {"simple", "martial"})

            return "martial" in proficiencies

        if isinstance(item, Armour):
            return any(
                p.name == item.proficiency_group
                for p in self.get_armour_proficiencies()
            )

        if isinstance(item, Tool):
            return any(
                p.name.casefold() == item.proficiency_group.casefold()
                for p in self.get_tool_proficiencies()
            )

        return False

    # --------------------------------------------------------
    # GENERAL QUERIES
    # --------------------------------------------------------

    def knows_language(self, language: str) -> bool:
        return any(
            proficiency.name.casefold() == language.casefold()
            for proficiency in self.get_languages()
        )

    def get_hit_point_features(self) -> list[HitPoints]:
        return [
            feature
            for feature in self.get_features()
            if isinstance(feature, HitPoints)
        ]

    def get_speeds(self) -> dict[str, int]:
        """Return the highest recorded speed for each movement type."""

        speeds: dict[str, int] = {}

        for feature in self.get_features():
            if isinstance(feature, Speed):
                speeds[feature.movement_type] = max(
                    speeds.get(feature.movement_type, 0),
                    feature.amount,
                )

        return speeds

    def get_size(self) -> str | None:
        sizes = [
            feature.size
            for feature in self.get_features()
            if isinstance(feature, Size)
        ]
        return sizes[-1] if sizes else None

    @property
    def caster_level(self) -> int:
        """Effective level for shared Spellcasting slot progression."""

        total = sum(
            feature.amount
            for feature in self.get_features()
            if isinstance(feature, CasterLevel)
        )

        return min(math.ceil(total), 20)

    @property
    def spell_slots(self) -> dict[int, int]:
        """Shared multiclass Spellcasting slots, keyed by spell level."""

        level = self.caster_level

        if level < 1:
            return {}

        return {
            spell_level: count
            for spell_level, count in enumerate(
                MULTICLASS_SPELL_SLOTS[level],
                start=1,
            )
            if count > 0
        }

    def get_prepared_spell_count(self, pool_name: str) -> int | None:
        """Calculate the preparation limit for a supported pool rule."""

        pool = self.get_spell_pools()[pool_name]
        rule = pool.prepared_spell_rule

        if rule is None:
            return None

        if pool.ability is None:
            raise ValueError(
                f"Spell pool {pool_name!r} has a preparation rule "
                "but no spellcasting ability."
            )

        class_level = self.get_class_level(pool_name)
        ability_modifier = self.get_ability_modifier(pool.ability)

        if rule == "class_level_plus_ability_modifier":
            return max(1, class_level + ability_modifier)

        if rule == "half_class_level_plus_ability_modifier":
            return max(1, class_level // 2 + ability_modifier)

        if rule == "ability_modifier":
            return max(1, ability_modifier)

        if rule == "wizard_table":
            return WIZARD_PREPARED_SPELLS.get(class_level, 0)

        if rule == "all":
            return None

        raise ValueError(f"Unsupported preparation rule: {rule!r}")


# ============================================================
# LATEX OUTPUT
# ============================================================


def _escape_tex(text: str) -> str:
    replacements = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in text)


def _signed(value: int) -> str:
    return f"{value:+d}"


def _format_modifier(value: int) -> str:
    return str(value)


def _format_spell_damage_type(damage_type: str) -> str:
    mapping = {
        "piercing": "p",
        "slashing": "s",
        "bludgeoning": "b",
        "fire": "fire",
        "cold": "cold",
        "lightning": "lightning",
        "thunder": "thunder",
        "acid": "acid",
        "poison": "poison",
        "psychic": "psychic",
        "necrotic": "necrotic",
        "radiant": "radiant",
        "force": "force",
    }
    return mapping.get(damage_type.casefold(), damage_type)


def _skill_macro_name(skill_name: SkillName) -> str:
    mapping = {
        "acrobatics": "Acrobatics",
        "animal_handling": "AnimalHandling",
        "arcana": "Arcana",
        "athletics": "Athletics",
        "deception": "Deception",
        "history": "History",
        "insight": "Insight",
        "intimidation": "Intimidation",
        "investigation": "Investigation",
        "medicine": "Medicine",
        "nature": "Nature",
        "perception": "Perception",
        "performance": "Performance",
        "persuasion": "Persuasion",
        "religion": "Religion",
        "sleight_of_hand": "SleightOfHand",
        "stealth": "Stealth",
        "survival": "Survival",
    }
    return mapping[skill_name]


def _ability_macro_name(ability: Ability) -> str:
    mapping = {
        "strength": "Strength",
        "dexterity": "Dexterity",
        "constitution": "Constitution",
        "intelligence": "Intelligence",
        "wisdom": "Wisdom",
        "charisma": "Charisma",
    }
    return mapping[ability]


def _proficiency_text(
    *, proficient: bool = False, expert: bool = False, half: bool = False
) -> str:
    if expert:
        return "Expert"
    if proficient:
        return "Proficient"
    if half:
        return "Half"
    return ""


def _best_armour_and_ac(character: Character) -> tuple[int, str]:
    armours = [
        item
        for item in character.items
        if isinstance(item, Armour) and item.proficiency_group != "shields"
    ]
    shields = [
        item
        for item in character.items
        if isinstance(item, Armour) and item.proficiency_group == "shields"
    ]

    if armours:
        worn_armour = max(
            armours,
            key=lambda armour: character.get_armour_class(armour),
        )
        ac = character.get_armour_class(worn_armour)
        if shields:
            ac += sum(shield.base_ac for shield in shields)
        return ac, worn_armour.name

    ac = character.get_armour_class()
    if shields:
        ac += sum(shield.base_ac for shield in shields)
    return ac, "Unarmoured"


def _weapon_lines(character: Character) -> list[str]:
    lines: list[str] = []

    for item in character.items:
        if not isinstance(item, Weapon):
            continue

        attack = _signed(character.get_weapon_attack_bonus(item))
        damage = item.damage
        modifier = character.get_weapon_ability_modifier(item)
        if modifier:
            damage += f"{modifier:+d}"
        if item.damage_type:
            damage += f"/{_format_spell_damage_type(item.damage_type)}"

        lines.append(
            rf"\AddWeapon{{{_escape_tex(item.name)}}}{{{attack}}}{{{_escape_tex(damage)}}}"
        )

    return lines


def _combat_feature_text(character: Character) -> str:
    parts: list[str] = []

    for feature in character.get_features():
        if isinstance(feature, Feature) and feature.is_combat:
            text = rf"\textbf{{{_escape_tex(feature.name)}}}"
            if feature.description:
                text += rf" \\ \textit{{{_escape_tex(feature.description)}}}"
            text += r" \\"
            parts.append(text)

    return "\n".join(parts)


def _features_text(character: Character) -> str:
    parts = [r"\textbf{Features} \\"]

    for feature in character.get_features():
        if not isinstance(feature, Feature) or feature.is_combat:
            continue

        parts.append(rf"\textbf{{{_escape_tex(feature.name)}}} \\")
        if feature.description:
            parts.append(rf"\textit{{{_escape_tex(feature.description)}}} \\")

    return "\n".join(parts)


def _other_proficiencies_text(character: Character) -> str:
    languages = (
        ", ".join(_escape_tex(p.name) for p in character.get_languages())
        or "None"
    )
    weapons = (
        ", ".join(
            _escape_tex(p.name.title())
            for p in character.get_weapon_proficiencies()
        )
        or "None"
    )
    armour = (
        ", ".join(
            _escape_tex(p.name.title())
            for p in character.get_armour_proficiencies()
        )
        or "None"
    )
    tools = (
        ", ".join(
            _escape_tex(p.name) for p in character.get_tool_proficiencies()
        )
        or "None"
    )

    return "\n".join(
        [
            rf"\textbf{{Languages:}} {languages}. \\",
            rf"\textbf{{Weapons:}} {weapons}. \\",
            rf"\textbf{{Armor:}} {armour}. \\",
            rf"\textbf{{Other:}} {tools}. \\",
        ]
    )


def _equipment_text(character: Character) -> str:
    mundane: list[str] = []
    magic: list[str] = []

    for item in character.items:
        if isinstance(item, (Weapon, Armour, Tool)):
            continue

        name = _escape_tex(item.name)
        if item.quantity != 1:
            name = f"{item.quantity}x {name}"

        if isinstance(item, Magic):
            magic.append(name)
        else:
            mundane.append(name)

    parts: list[str] = []

    if mundane:
        parts.append(", ".join(mundane) + r" \\")
    if magic:
        parts.append(r"\textbf{Magic Items:} " + ", ".join(magic) + r" \\")

    return "\n".join(parts)


def _spell_slot_total(character: Character, level: int) -> int:
    return character.spell_slots.get(level, 0)


def _spell_lines_for_level(character: Character, spell_level: int) -> list[str]:
    entries: list[tuple[str, SpellAccess]] = []

    for pool_name, pool in character.get_spell_pools().items():
        for access in pool.spells:
            if access.spell.level == spell_level:
                entries.append((pool_name, access))

    entries.sort(key=lambda entry: entry[1].spell.name)

    lines: list[str] = []
    for pool_name, access in entries[:5]:
        spell = access.spell
        text = _escape_tex(spell.name)
        if pool_name:
            text += f" ({_escape_tex(pool_name)})"
        if spell.reference and spell.reference.page:
            text += f" ({_escape_tex(spell.reference.source)} {spell.reference.page})"
        lines.append(text)

    return lines


def _cantrip_lines(character: Character) -> list[str]:
    entries: list[tuple[str, SpellAccess]] = []

    for pool_name, pool in character.get_spell_pools().items():
        for access in pool.spells:
            if access.spell.level == 0:
                entries.append((pool_name, access))

    entries.sort(key=lambda entry: entry[1].spell.name)

    return [_escape_tex(access.spell.name) for _, access in entries[:8]]


def render_sheet_tex(character: Character) -> str:
    abilities = [
        "strength",
        "dexterity",
        "constitution",
        "intelligence",
        "wisdom",
        "charisma",
    ]

    class_text = " / ".join(
        f"{character.get_class_level(cls)} {subclass[0] if (subclass := [x.subclass.name for x in character.classes if x.name == cls and getattr(x, 'subclass', None) is not None]) else cls}"
        for cls in {x.name for x in character.classes}
    )

    ac, _ = _best_armour_and_ac(character)
    speeds = character.get_speeds()
    walking_speed = speeds.get("walking", 0)

    skill_map = {skill.name: skill for skill in character.get_skills()}
    save_map = {save.name: save for save in character.get_saving_throws()}

    perception = character.get_skill_modifier("perception")

    pools = character.get_spell_pools()

    lines: list[str] = [
        r"\documentclass[letterpaper,openany,oneside,twocolumn]{book}",
        r"\usepackage{bookmark}",
        r"\usepackage[justified]{dnd}",
        r"\usepackage{ifthen}",
        r"\usepackage{geometry}",
        r"\usepackage{pstricks}",
        "",
        r"\usepackage{dndtemplate}",
        "",
        r"\setlength\oddsidemargin{\dimexpr(\paperwidth-\textwidth)/2 - 1in\relax}",
        r"\setlength\evensidemargin{\oddsidemargin}",
        "",
        rf"\CharacterName{{{_escape_tex(character.name)}}}",
        "",
        rf"\Class{{{_escape_tex(class_text)}}}",
        rf"\Background{{{_escape_tex(character.background.name if character.background else '')}}}",
        r"\PlayerName{}",
        rf"\Race{{{_escape_tex(character.race.name if character.race else '')}}}",
        r"\Alignment{}",
        r"\XP{Milestone}",
        "",
    ]

    for ability in abilities:
        macro = _ability_macro_name(ability)
        lines.append(
            rf"\{macro}Score{{{character.get_ability_score(ability)}}}"
        )

    lines.append("")

    for ability in abilities:
        macro = _ability_macro_name(ability)
        lines.append(
            rf"\{macro}Modifier{{{_format_modifier(character.get_ability_modifier(ability))}}}"
        )

    lines.append("")

    for ability in abilities:
        macro = _ability_macro_name(ability)
        lines.append(
            rf"\{macro}SavingThrowModifier{{{_format_modifier(character.get_saving_throw_modifier(ability))}}}"
        )

    lines.append("")

    for skill_name in SKILL_ABILITIES:
        macro = _skill_macro_name(skill_name)
        lines.append(
            rf"\{macro}SkillModifier{{{_format_modifier(character.get_skill_modifier(skill_name))}}}"
        )

    lines.extend(
        [
            "",
            rf"\StrengthProficiency{{{_proficiency_text(proficient=bool(save_map.get('strength') and save_map['strength'].proficient))}}}",
            rf"\DexterityProficiency{{{_proficiency_text(proficient=bool(save_map.get('dexterity') and save_map['dexterity'].proficient))}}}",
            rf"\ConstitutionProficiency{{{_proficiency_text(proficient=bool(save_map.get('constitution') and save_map['constitution'].proficient))}}}",
            rf"\IntelligenceProficiency{{{_proficiency_text(proficient=bool(save_map.get('intelligence') and save_map['intelligence'].proficient))}}}",
            rf"\WisdomProficiency{{{_proficiency_text(proficient=bool(save_map.get('wisdom') and save_map['wisdom'].proficient))}}}",
            rf"\CharismaProficiency{{{_proficiency_text(proficient=bool(save_map.get('charisma') and save_map['charisma'].proficient))}}}",
        ]
    )

    for skill_name in SKILL_ABILITIES:
        skill = skill_map.get(skill_name)
        proficiency = ""
        if skill:
            proficiency = _proficiency_text(
                proficient=skill.proficient,
                expert=skill.expertise,
            )
        lines.append(
            rf"\{_skill_macro_name(skill_name)}Proficiency{{{proficiency}}}"
        )

    lines.extend(
        [
            "",
            r"\Inspiration{}",
            rf"\Proficiency{{{character.get_proficiency_bonus()}}}",
            rf"\Perception{{{perception}}}",
            "",
            rf"\ArmorClass{{{ac}}}",
            rf"\Initiative{{{character.get_initiative_modifier()}}}",
            rf"\Speed{{{walking_speed}}}",
            rf"\MaxHitPoints{{{character.get_max_hp()}}}",
            "",
        ]
    )

    hit_dice_parts = []
    for class_name in dict.fromkeys(cls.name for cls in character.classes):
        class_levels = [
            cls for cls in character.classes if cls.name == class_name
        ]
        hit_die = class_levels[0].hit_die
        level_count = character.get_class_level(class_name)
        hit_dice_parts.append(f"{level_count}d{hit_die}")

    lines.extend(
        [
            rf"\MaxHitDice{{{_escape_tex(' + '.join(hit_dice_parts))}}}",
            "",
            r"\CP{}",
            r"\SP{}",
            r"\GP{}",
            r"\EP{}",
            r"\PP{}",
            "",
        ]
    )

    lines.extend(_weapon_lines(character))
    lines.append("")

    lines.append(rf"\AttacksAdditional{{{_combat_feature_text(character)}}}")
    lines.append("")
    lines.append(
        rf"\OtherProficienciesLanguages{{{_other_proficiencies_text(character)}}}"
    )
    lines.append("")
    lines.append(rf"\Equipment{{{_equipment_text(character)}}}")
    lines.append("")

    lines.append(rf"\PersonalityTraits{{{_escape_tex(character.personality)}}}")
    lines.append(rf"\Ideals{{{_escape_tex(character.ideals)}}}")
    lines.append(rf"\Bonds{{{_escape_tex(character.bonds)}}}")
    lines.append(rf"\Flaws{{{_escape_tex(character.flaws)}}}")
    lines.append("")
    lines.append(rf"\FeaturesTraits{{{_features_text(character)}}}")
    lines.append("")

    lines.extend(
        [
            r"\Age{}",
            r"\Height{}",
            r"\Weight{}",
            r"\Eyes{}",
            r"\Skin{}",
            r"\Hair{}",
            "",
        ]
    )

    spell_class = "/".join(
        [
            f"{pool} (P {character.get_prepared_spell_count(pool)})"
            if character.get_prepared_spell_count(pool)
            else pool
            for pool in pools.keys()
        ]
        )
    spell_ability = set([pool.ability for pool in pools.values()])
    ability_string = "/".join(
        {_escape_tex(ability[:3].upper()) for ability in spell_ability}
    )
    spell_save_string = "/".join(
        [str(character.get_spell_save_dc(ability)) for ability in spell_ability]
    )
    spell_attack_string = "/".join(
        [
            _signed(character.get_spell_attack_bonus(ability))
            for ability in spell_ability
        ]
    )

    lines.extend(
        [
            rf"\SpellcastingClass{{{_escape_tex(spell_class)}}}",
            rf"\SpellcastingAbility{{{_escape_tex(ability_string)}}}",
            rf"\SpellSaveDC{{{_escape_tex(spell_save_string)}}}",
            rf"\SpellAttackBonus{{{_escape_tex(spell_attack_string)}}}",
        ]
    )

    for level in range(0, 10):
        if level != 0:
            lines.extend(
                [
                    rf"\{ordinal_dict[level]}LevelSpellSlotsTotal{{{_spell_slot_total(character, level)}}}"
                ]
            )

        slot_index = 0

        for name, pool in pools.items():
            if level == 0:
                cantrips = pool.get_spells_by_level(0)
                for cantrip in cantrips:
                    slot_name = f"CantripSlot{chr(ord('A') + slot_index)}"
                    slot_index += 1

                    base_string = cantrip.spell.name
                    if len(pools) > 1:
                        base_string += f" ({name})"
                    if len(spell_ability) > 1 or cantrip.ability_override:
                        base_string += f" ({pool.ability[:3].upper() if not cantrip.ability_override else cantrip.ability_override[:3].upper()})"
                    if cantrip.spell.reference:
                        base_string += cantrip.spell.reference.to_string()

                    lines.append(rf"\{slot_name}{{{base_string}}}")
            else:
                spells = pool.get_spells_by_level(level)
                for spell in spells:
                    slot_name = f"LevelSpellSlot{chr(ord('A') + slot_index)}"
                    slot_index += 1
                    base_string = spell.spell.name
                    if spell.spell.ritual:
                        base_string += f" R"
                    if len(pools) > 1:
                        base_string += f" ({name})"
                    if len(spell_ability) > 1 or spell.ability_override:
                        base_string += f" ({pool.ability[:3].upper() if not spell.ability_override else spell.ability_override[:3].upper()})"
                    if spell.spell.reference:
                        base_string += spell.spell.reference.to_string()

                    lines.append(
                        rf"\{ordinal_dict[level]}{slot_name}{{{base_string}}}"
                    )
                    if spell.preparation != "known":
                        lines.append(
                            rf"\{ordinal_dict[level]}{slot_name}Prepared{{True}}"
                        )


    lines.extend(
        [
            "",
            r"\newcommand{\spellsheetchoice}{\renderspellsheet}",
            "",
            r"\begin{document}",
            r"\newgeometry{left=0cm,right=0cm,top=0cm,bottom=0cm}",
            r"\onecolumn",
            "",
            r"\pdfbookmark[0]{Character Sheet}{Character Sheet}",
            r"\rendercharactersheet",
            "",
            r"\pdfbookmark[0]{Spellcasting Sheet}{Spellcasting Sheet}",
            r"\spellsheetchoice",
            "",
            r"\end{document}",
        ]
    )

    return "\n".join(lines)


# ============================================================
# EXAMPLE CHARACTER
# ============================================================

level_1_pool = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Prestidigitation", 0, school="transmutation")),
        SpellAccess(Spell("Message", 0, school="transmutation")),
        SpellAccess(Spell("Light", 0, school="transmutation")),
        SpellAccess(Spell("Detect Magic", 1, school="divination", ritual=True)),
        SpellAccess(
            Spell("Find Familiar", 1, school="conjuration", ritual=True)
        ),
        SpellAccess(Spell("Fog Cloud", 1, school="conjuration")),
        SpellAccess(Spell("Mage Armour", 1, school="abjuration")),
        SpellAccess(Spell("Disguise Self", 1, school="illusion")),
        SpellAccess(
            Spell("Illusory Script", 1, school="illusion", ritual=True)
        ),
    ],
)

wizard_level_1 = ClassLevel(
    name="Wizard",
    level=1,
    hit_die=6,
    hp_roll=4,
    reference=Reference(page=165),
    features=[
        Skill(name="history"),
        Skill(name="investigation"),
        SavingThrow(name="wisdom"),
        SavingThrow(name="intelligence"),
        WeaponProficiency(name="simple"),
        CasterLevel(amount=1),
        Feature(
            name="Arcane Recovery",
            description=(
                "Recover spell slots with a combined level equal to "
                "half your Wizard level (rounded up) once per long rest."
            ),
        ),
    ],
    spell_pools=[level_1_pool],
)

level_2_pool = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Sleep", 1, school="enchantment")),
        SpellAccess(Spell("Identify", 1, school="divination", ritual=True)),
    ],
)

wizard_level_2 = ClassLevel(
    name="Wizard",
    level=2,
    hit_die=6,
    hp_roll=3,
    reference=Reference(page=165),
    features=[
        Skill(name="investigation", expertise=True, proficient=False),
        CasterLevel(amount=1),
    ],
    spell_pools=[level_2_pool],
)

level_3_pool = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Mirror Image", 2, school="illusion")),
        SpellAccess(Spell("Detect Thoughts", 2, school="divination")),
    ],
)

illusion_savant = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Invisibility", 2, school="illusion")),
        SpellAccess(Spell("Phantasmal Force", 2, school="illusion")),
    ],
)

wizard_level_3 = ClassLevel(
    name="Wizard",
    level=3,
    hit_die=6,
    hp_roll=3,
    reference=Reference(page=165),
    features=[CasterLevel(amount=1)],
    subclass=Source(
        name="Illusionist",
        reference=Reference(page=175),
        spell_pools=[illusion_savant],
        features=[
            Feature(
                name="Improved Illusions",
                description=(
                    "Increase the range of illusion spells by 60 feet. "
                    "Minor Illusion becomes a Bonus Action and can create "
                    "sound and image together."
                ),
            )
        ],
    ),
    spell_pools=[level_3_pool],
)

rouge_level_1 = ClassLevel(
    name="Rogue",
    level=1,
    hit_die=8,
    hp_roll=7,
    reference=Reference(page=129),
    features=[
        ToolProficiency(name="Poisoners Tools"),
        WeaponProficiency(name="martial"),
        Skill("insight"),
        Skill("stealth", expertise=True),
        Skill("sleight_of_hand", expertise=True),
        LanguageProficiency("Undercommon"),
        Feature(
            name="Sneak Attack",
            description=("Add 1d6 to a roll if you have advantage"),
        ),
    ],
)
rouge_level_2 = ClassLevel(
    name="Rogue",
    level=2,
    hit_die=8,
    hp_roll=7,
    reference=Reference(page=129),
    features=[
        Feature(
            name="Cunning Action",
            description=("Bonus Action Dash, Disengage or Hide"),
        ),
    ],
)
rouge_3_spell_pool = SpellPool(
    name="Rouge",
    ability="intelligence",
    prepared_spell_rule="all",
    spells=[
        SpellAccess(
            Spell("Tasha's Hideous Laughter", 1, school="enchantment"),
            preparation="always_prepared",
        ),
        SpellAccess(
            Spell("Charm Person", 1, school="enchantment"),
            preparation="always_prepared",
        ),
        SpellAccess(
            Spell("Shield", 1, school="abjuration"),
            preparation="always_prepared",
        ),
        SpellAccess(Spell("Mind Sliver", 0, school="enchantment")),
        SpellAccess(Spell("Mage Hand", 0, school="conjuration")),
        SpellAccess(Spell("Friends", 0, school="enchantment")),
    ],
)


rouge_level_3 = ClassLevel(
    name="Rogue",
    level=3,
    hit_die=8,
    hp_roll=7,
    reference=Reference(page=129),
    subclass=Source(
        name="Arcane Trickster",
        reference=Reference(page=132),
        features=[
            Feature(
                name="Mage Hand Legerdemain",
                description="Mage Hand can be cast as a bonus action and is invisible; it can be used for Dex checks.",
            ),
            CasterLevel(0.33),
        ],
        spell_pools=[rouge_3_spell_pool],
    ),
    features=[
        Feature(
            name="Improved Sneak Attack",
            description="Add 2d6 to a roll if you have advantage",
        ),
        Feature(
            name="Steady Aim",
            description="Bonus Action Dash, Disengage or Hide",
        ),
    ],
)


all_classes = [
    wizard_level_1,
    wizard_level_2,
    wizard_level_3,
    rouge_level_1,
    rouge_level_2,
    rouge_level_3,
]

pebble = Character(
    name="Pebble",
    abilities={
        "strength": 10,
        "dexterity": 14,
        "constitution": 14,
        "intelligence": 15,
        "wisdom": 10,
        "charisma": 8,
    },
    background=Source(
        name="Criminal",
        features=[
            AbilityScore(name="intelligence", amount=1),
            AbilityScore(name="dexterity", amount=2),
            Skill(name="sleight_of_hand"),
            Skill(name="stealth"),
            ToolProficiency(name="Thieve's tools"),
        ],
        reference=Reference(page=179),
        sources=[
            Source(
                name="Alert",
                reference=Reference(page=200),
                features=[
                    InitiativeProficiency(),
                    Feature(
                        name="Initiative Swap",
                        description=(
                            "Swap initiative with a willing character."
                        ),
                    ),
                ],
            )
        ],
    ),
    race=Source(
        name="Dwarf",
        reference=Reference(page=188),
        features=[HitPoints(amount=1)] * len(all_classes)
        + [
            Size("medium"),
            Speed(30),
            Feature(
                name="Darkvision",
                description=("See in dim light and darkness within 60 feet."),
            ),
            Feature(
                name="Dwarven Resilience",
                description="Advantage against poison; resistance to poison damage.",
            ),
            Feature(
                name="Stone Cunning",
                description=(
                    "Bonus Action: gain 60-foot Tremorsense for 10 minutes."
                ),
            ),
            LanguageProficiency("Common"),
            LanguageProficiency("Common Sign"),
            LanguageProficiency("Common Dwarvish"),
        ],
    ),
    features=[
        Feature(
            "Drake Knowledge", description="Advantage on checks against Drakes"
        )
    ],
    classes=all_classes,
    items=[
        # Weapons
        Weapon(
            name="Dagger",
            quantity=6,
            damage="1d4",
            damage_type="piercing",
            properties=["Finesse", "Light", "Thrown 20/60"],
        ),
        Weapon(
            name="Quarterstaff",
            damage="1d6",
            damage_type="bludgeoning",
            properties=["Versatile (1d8)"],
        ),
        # Tools
        Tool(
            name="Thieve's tools",
            proficiency_group="Thieve's tools",
        ),
        # Adventuring gear
        MiscItem(name="Traveller's Clothes", quantity=1),
        MiscItem(name="Book", quantity=1),
        MiscItem(name="Crowbar", quantity=1),
        MiscItem(name="Ink", quantity=1),
        MiscItem(name="Ink Pen", quantity=1),
        MiscItem(name="Lamp", quantity=1),
        MiscItem(name="Oil", quantity=10),
        MiscItem(name="Parchment", quantity=10),
        MiscItem(name="Robe", quantity=1),
        MiscItem(name="Tinderbox", quantity=1),
        MiscItem(name="Whalebone Necklace", quantity=1),
        # Magic items — none require attunement
        MagicMiscItem(
            name="Moonstone Boots",
            quantity=1,
            description=(
                "Increases jumping distance by an additional 200% "
                "and allows the wearer to land quietly."
            ),
            rarity="Unknown",
            requires_attunement=False,
        ),
        MagicMiscItem(
            name="Purple Cloak with Deep Pockets",
            quantity=1,
            description=(
                "A purple cloak with exceptionally deep pockets, "
                "providing storage approaching that of a Bag of Holding."
            ),
            rarity="Unknown",
            requires_attunement=False,
        ),
        MagicMiscItem(
            name="Fog-Piercing Spyglass",
            quantity=1,
            description="Allows the user to see through fog.",
            rarity="Unknown",
            requires_attunement=False,
        ),
    ],
)
character = pebble

print(render_sheet_tex(pebble))
