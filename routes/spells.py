from fastapi import APIRouter
from typing import List, Optional
from models.spell import Spell

router = APIRouter()

spells_db = [
    Spell(id=1, name="Fireball", level=3, school="Evocation",
          description="A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame.",
          image_url="http://127.0.0.1:8000/static/images/fireball.png"
          ),
    Spell(id=2, name="Healing Word", level=1, school="Evocation",
          description="A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier.",
          image_url="http://127.0.0.1:8000/static/images/heart.png"),
    Spell(id=3, name="Mage Armor", level=1, school="Abjuration",
          description="You touch a willing creature who isn't wearing armor, and a protective magical force surrounds it until the spell ends.",
          image_url="http://127.0.0.1:8000/static/images/shield.png"),
    Spell(id=4, name="Lightning Bolt", level=3, school="Evocation",
          description="A stroke of lightning forming a line 100 feet long and 5 feet wide blasts out from you in a direction you choose.",
          image_url="http://127.0.0.1:8000/static/images/lightning.png"),
    Spell(id=7, name="Acid Splash", level=1, school="Conjuration",
          description="You hurl a bubble of acid at a creature within range. The target must succeed on a Dexterity saving throw or take 1d6 acid damage.",
          image_url="http://127.0.0.1:8000/static/images/flask.png")
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
