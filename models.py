from pydantic import BaseModel, Field
from typing import List

class Party (BaseModel):
    name: str
    color: str
    prc_votes: float = Field(le=100,ge=0)
    seats:int = Field(le=240,ge=0,default=0)


all_parties: List[Party] = [
    Party(
        name="Radev",
        color="#10410A",
        prc_votes=32.5
    ),
    Party(
        name="GERB",
        color="#0054A6",
        prc_votes=21.2
    ),
    Party(
        name="PP-DB",
        color="#FFD700", 
        prc_votes=14.8
    ),
    Party(
        name="Vazrazhdane",
        color="#000000",
        prc_votes=12.1
    ),
    Party(
        name="DPS", 
        color="#3C0652",
        prc_votes=8.4
    ),
    Party(
        name="ITN",
        color="#C1831F",
        prc_votes=4.5
    ),
    Party(
        name="BSP",
        color="#CC1414",
        prc_votes=4.0

    )
]