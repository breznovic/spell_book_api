from fastapi import APIRouter
from typing import List, Optional
from models.spell import Spell

router = APIRouter()

spells_db = [
    Spell(id=1, name="Fireball", level=3, school="Evocation",
          description="A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame."),
    Spell(id=2, name="Healing Word", level=1, school="Evocation",
          description="A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier."),
    Spell(id=3, name="Mage Armor", level=1, school="Abjuration",
          description="You touch a willing creature who isn't wearing armor, and a protective magical force surrounds it until the spell ends."),
    Spell(id=4, name="Lightning Bolt", level=3, school="Evocation",
          description="A stroke of lightning forming a line 100 feet long and 5 feet wide blasts out from you in a direction you choose."),
    Spell(id=5, name="Shield", level=1, school="Abjuration",
          description="An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC.")
]


@router.get("/", response_model=List[Spell])
def get_spells():
    return spells_db


@router.post("/", response_model=Spell)
def create_spell(spell: Spell):
    spells_db.append(spell)
    return spell


@router.get("/{spell_id}", response_model=Optional[Spell])
def get_spell(spell_id: int):
    for spell in spells_db:
        if spell.id == spell_id:
            return spell
    return None
