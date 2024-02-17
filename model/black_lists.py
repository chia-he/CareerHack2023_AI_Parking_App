from typing import Optional
from pydantic import BaseModel

class Black_Lists(BaseModel):
    BL_LICENSE : str
    BL_STARTTIME : str
    BL_ENDTIME : str