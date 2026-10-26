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

from characters.pebbel_2 import pebble

level_3_pool = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Suggestion", 2, school="enchantment")),
        SpellAccess(Spell("Detect Thoughts", 2, school="divination")),
    ],
)

illusion_savant = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Invisibility", 2, school="illusion")),
        SpellAccess(Spell("Blur", 2, school="illusion")),
    ],
)

better_minor_illusion = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Mage Hand", 0)),
    ],
)

wizard_level_3 = ClassLevel(
    name="Wizard",
    level=3,
    hit_die=6,
    hp_roll=5,
    reference=Reference(page=165),
    features=[CasterLevel(amount=1)],
    subclass=Source(
        name="Illusionist",
        reference=Reference(page=175),
        spell_pools=[illusion_savant, better_minor_illusion],
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

pebble.classes.append(wizard_level_3)

pebble.race.features.append(HitPoints(amount=1))
