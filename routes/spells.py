from fastapi import File, UploadFile, Form, HTTPException, APIRouter
from typing import List, Optional
from models.spell import Spell

router = APIRouter()

spells_db: List[Spell] = [
    Spell(id=1, name="Fireball", level=3, school="Evocation",
          description="A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame.",
          image_url="http://localhost:8001/static/images/fireball.png"
          ),
    Spell(id=2, name="Healing Word", level=1, school="Evocation",
          description="A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier.",
          image_url="http://localhost:8001/static/images/heart.png"),
    Spell(id=3, name="Mage Armor", level=1, school="Abjuration",
          description="You touch a willing creature who isn't wearing armor, and a protective magical force surrounds it until the spell ends.",
          image_url="http://localhost:8001/static/images/shield.png"),
    Spell(id=4, name="Lightning Bolt", level=3, school="Evocation",
          description="A stroke of lightning forming a line 100 feet long and 5 feet wide blasts out from you in a direction you choose.",
          image_url="http://localhost:8001/static/images/lightning.png"),
    Spell(id=5, name="Acid Splash", level=1, school="Conjuration",
          description="You hurl a bubble of acid at a creature within range. The target must succeed on a Dexterity saving throw or take 1d6 acid damage.",
          image_url="http://localhost:8001/static/images/flask.png"),
    Spell(id=6, name="Invisibility", level=2, school="Illusion",
          description="A creature you touch becomes invisible until the spell ends. Anything the target is wearing or carrying is invisible as long as it is on the target's person.",
          image_url="http://localhost:8001/static/images/invisible.png"
          ),
    Spell(id=7, name="Magic Missile", level=1, school="Evocation",
          description="You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range.",
          image_url="http://localhost:8001/static/images/missile.png"),
    Spell(id=8, name="Web", level=2, school="Conjuration",
          description="You conjure a mass of thick, sticky webbing at a point within range. The area is difficult terrain, and creatures can become restrained.",
          image_url="http://localhost:8001/static/images/web.png"),
    Spell(id=9, name="Fire Shield", level=4, school="Abjuration",
          description="You create a protective magical force that surrounds you, granting you resistance to cold or fire damage.",
          image_url="http://localhost:8001/static/images/fire_shield.png"),
    Spell(id=10, name="Fog Cloud", level=1, school="Conjuration",
          description="You create a 20-foot-radius sphere of fog centered on a point within range. The area is heavily obscured.",
          image_url="http://localhost:8001/static/images/fog.png"),
]


def get_new_spell_id():
    if not spells_db:
        return 1
    return max(spell.id for spell in spells_db) + 1


@router.get("/", response_model=List[Spell])
def get_spells():
    return spells_db


@router.get("/{spell_id}", response_model=Optional[Spell])
def get_spell(spell_id: int):
    for spell in spells_db:
        if spell.id == spell_id:
            return spell
    return None


@router.post("/")
async def create_spell(
    name: str = Form(...),
    description: str = Form(...),
    level: int = Form(...),
    school: str = Form(...),
    imageUrl: Optional[UploadFile] = File(None),
):
    try:
        new_id = get_new_spell_id()
        image_url = None

        if imageUrl:
            file_location = f"static/images/{imageUrl.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await imageUrl.read())
            image_url = f"http://localhost:8001/{file_location}"
        else:
            image_url = "http://localhost:8001/static/images/default_spell_image.png"

        new_spell = Spell(
            id=new_id,
            name=name,
            level=level,
            school=school,
            description=description,
            image_url=image_url,
        )

        spells_db.append(new_spell)
        return new_spell

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{spell_id}")
async def update_spell(
    spell_id: int,
    name: str = Form(None),
    description: str = Form(None),
    level: int = Form(None),
    school: str = Form(None),
    imageUrl: Optional[UploadFile] = File(None),
):
    try:
        spell_to_update = next(
            (spell for spell in spells_db if spell.id == spell_id), None)
        if not spell_to_update:
            raise HTTPException(status_code=404, detail="Spell not found")

        if name:
            spell_to_update.name = name
        if description:
            spell_to_update.description = description
        if level:
            spell_to_update.level = level
        if school:
            spell_to_update.school = school

        if imageUrl:
            file_location = f"static/images/{imageUrl.filename}"
            with open(file_location, "wb+") as file_object:
                file_object.write(await imageUrl.read())
            spell_to_update.image_url = f"http://localhost:8001/{file_location}"
        else:
            spell_to_update.image_url = "http://localhost:8001/static/images/default_spell_image.png"

        return spell_to_update

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{spell_id}", status_code=204)
async def delete_spell(spell_id: int):
    global spells_db
    spells_db = [spell for spell in spells_db if spell.id != spell_id]
