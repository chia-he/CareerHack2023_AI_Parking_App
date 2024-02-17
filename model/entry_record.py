from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Enter_Record(BaseModel):
    ER_PLID : str
    ER_LICENSE : str
    ER_ENTER_TIME : Optional[datetime]
    ER_EXIT_TIME: Optional[datetime]
    ER_IMAGE: str