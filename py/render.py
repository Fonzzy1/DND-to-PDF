from .character import Character
from .constants import Ability, SKILL_ABILITIES, ordinal_dict
from .features import Feature, Skill, SavingThrow
from .items import Armour, Magic, Tool, Weapon
from .spells import SpellAccess


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


def _skill_macro_name(skill_name: str) -> str:
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
        # r"\usepackage[justified]{dnd}",
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

