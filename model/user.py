from pydantic import BaseModel
from typing import Union, Optional

class User(BaseModel):
    NAME: str
    USERNAME: str
    PASSWORD: str
    NUMBER: Optional[str]
    COMPANY: Optional[str]
    LICENSE: str
    EMAIL: Union[str, None] = None