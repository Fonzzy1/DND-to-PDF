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

level_1_pool = SpellPool(
    name="Wizard",
    ability="intelligence",
    prepared_spell_rule="wizard_table",
    spells=[
        SpellAccess(Spell("Prestidigitation", 0, school="transmutation")),
        SpellAccess(Spell("Message", 0, school="evocation")),
        SpellAccess(Spell("Minor Illusion", 0, school="illusion")),
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


all_classes = [
    wizard_level_1,
    wizard_level_2,
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
