from pydantic import BaseModel


class Park(BaseModel):
    PA_PLID : str
    PA_PSID : str
    PA_LICENSE : str
    PA_IMAGE : str