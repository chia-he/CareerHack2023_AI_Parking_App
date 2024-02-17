from pydantic import BaseModel

class Staff(BaseModel):
    ST_ID : str
    ST_NAME : str
    ST_NUMBER : str
    ST_EMAIL: str
    ST_USERNAME : str
    ST_PASSWORD : str