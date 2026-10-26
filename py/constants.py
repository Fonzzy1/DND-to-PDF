from typing import Literal

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

