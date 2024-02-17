from typing import Optional
from pydantic import BaseModel

class Security_Guard(BaseModel):
    SG_USERNAME : str
    SG_PASSWORD : str