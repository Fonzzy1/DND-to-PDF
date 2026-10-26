from py import (
    AbilityScore,
    CasterLevel,
    Character,
    ClassLevel,
    Feature,
    HitPoints,
    InitiativeProficiency,
    LanguageProficiency,
    MagicMiscItem,
    MiscItem,
    Reference,
    SavingThrow,
    Size,
    Skill,
    Source,
    Speed,
    Spell,
    SpellAccess,
    SpellPool,
    Tool,
    ToolProficiency,
    Weapon,
    WeaponProficiency,
)

from characters.pebbel_1 import pebble



level_2_pool = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Silent Image", 1, school="Illusion")),
        SpellAccess(Spell("Identify", 1, school="divination", ritual=True)),
    ],
)

wizard_level_2 = ClassLevel(
    name="Wizard",
    level=2,
    hit_die=6,
    hp_roll=4,
    reference=Reference(page=165),
    features=[
        Skill(name="investigation", expertise=True, proficient=False),
        CasterLevel(amount=1),
    ],
    spell_pools=[level_2_pool],
)

pebble.classes.append(wizard_level_2)

pebble.race.features.append(HitPoints(amount=1))

