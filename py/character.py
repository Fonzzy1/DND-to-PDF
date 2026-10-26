import math
from dataclasses import dataclass, field
from warnings import warn

from .constants import (
    Ability,
    Class,
    MULTICLASS_SPELL_SLOTS,
    SKILL_ABILITIES,
    SkillName,
    WIZARD_PREPARED_SPELLS,
)
from .features import (
    AbilityScore,
    ArmourProficiency,
    CasterLevel,
    CharacterFeature,
    HitPoints,
    Initiative,
    InitiativeProficiency,
    LanguageProficiency,
    SavingThrow,
    Size,
    Skill,
    Speed,
    ToolProficiency,
    WeaponProficiency,
)
from .items import Armour, Item, Tool, Weapon
from .models import ClassLevel, Source
from .spells import Spell, SpellAccess, SpellPool


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

    personality: str = """1. I'm old enough to know better, experienced enough to do it anyway, and tired enough to complain about it. I meet most things with dry humour and a healthy dose of cynicism.

    2. I get on well enough with ordinary folk, especially people who remind me of home. Ask if I'm all right, though, and you'll get a joke for an answer."""
    ideals: str = """Responsibility. Gods, governments, and commanders are all very good at explaining why someone else should bear the cost of their decisions. I make my own calls now. If someone has to pay for them, I won't pretend the responsibility belongs to anyone else."""
    bonds: str = """Home. I still dream of retiring in the village where I grew up. I tell myself I need to make it safe before I return. There is always another threat to deal with, and perhaps that's just as well — I wouldn't know what to do with myself if I ever got there."""
    flaws: str = """1. I cannot leave well enough alone. I insist on doing things my way, ignore advice I don't fancy, and struggle to trust anyone else with control — even when they're better suited to the task.

    2. I hide behind the job. When things get personal, I make a joke, change the subject, or find the next piece of work. It's easier to be useful than to work out who I am without a purpose."""

    def get_initiative_modifier(self) -> int:
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

    def get_level(self) -> int:
        class_levels: dict[str, int] = {}

        for cls in self.classes:
            class_levels[cls.name] = max(
                class_levels.get(cls.name, 0),
                cls.level,
            )

        return sum(class_levels.values())

    def get_class_level(self, class_name: Class) -> int:
        return max(
            (cls.level for cls in self.classes if cls.name == class_name),
            default=0,
        )

    def get_proficiency_bonus(self) -> int:
        return 2 + max(0, self.get_level() - 1) // 4

    def get_features(self) -> list[CharacterFeature]:
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

    def get_spell_pools(self) -> dict[str, SpellPool]:
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
        spells: dict[str, Spell] = {}

        for _, access in self.get_spell_entries():
            spells.setdefault(access.spell.name, access.spell)

        return list(spells.values())

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

    def get_max_hp(self) -> int:
        con_modifier = self.get_ability_modifier("constitution")

        total = sum(cls.hp_roll + con_modifier for cls in self.classes)

        total += sum(
            feature.amount
            for feature in self.get_features()
            if isinstance(feature, HitPoints)
        )

        return total

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

    def get_weapon_ability_modifier(self, weapon: Weapon) -> int:
        properties = {prop.casefold() for prop in weapon.properties}

        if "finesse" in properties:
            return max(
                self.get_ability_modifier("strength"),
                self.get_ability_modifier("dexterity"),
            )

        return self.get_ability_modifier("strength")

    def get_weapon_attack_bonus(self, weapon: Weapon) -> int:
        bonus = self.get_weapon_ability_modifier(weapon)

        if self.check_proficiency(weapon):
            bonus += self.get_proficiency_bonus()

        return bonus

    def get_weapon_damage(self, weapon: Weapon) -> str:
        modifier = self.get_weapon_ability_modifier(weapon)
        damage = weapon.damage

        if modifier:
            damage += f"{modifier:+d}"

        if weapon.damage_type:
            damage += f" {weapon.damage_type}"

        return damage

    def get_armour_class(self, armour: Armour | None = None) -> int:
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
        total = sum(
            feature.amount
            for feature in self.get_features()
            if isinstance(feature, CasterLevel)
        )

        return min(math.ceil(total), 20)

    @property
    def spell_slots(self) -> dict[int, int]:
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

