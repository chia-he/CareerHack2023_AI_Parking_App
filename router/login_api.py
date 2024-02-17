from datetime import datetime, timedelta
from typing import Union
from fastapi.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from pydantic import BaseModel

from controller import staff, vip

router = APIRouter()
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    ID: str
    USERNAME: str
    EMAIL: Union[str, None] = None
    NAME: Union[str, None] = None
    PASSWORD: Union[str, None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(ST_ID: str):
    result = await staff.get_STAFF_by_ST_ID(ST_ID)
    if len(result['response']) > 0:
        return await result
    else:
        return await {"msg": "success", "response":result} 

async def authenticate_user(request):
    form = await request.form()
    identify = form.get('identify')
    username = form.get('username')
    password = form.get('password')
    if identify == 'staff':
        result = await staff.get_STAFF_by_ST_USERNAME_and_ST_PASSWORD(username)
        
    elif identify == 'vip':
        result = await vip.get_VIP_by_VI_USERNAME_and_VI_PASSWORD(username)
    else:
        result = await staff.get_STAFF_by_ST_USERNAME_and_ST_PASSWORD(username)
    if len(result['response']) == 0:
        return False
    else:
        for r in result["response"]:
            if verify_password(password, r['PASSWORD']):
                user = User(**r)
                return user
        else:
            return False


@router.get("/app/login.html", tags=['get login Page'])
async def app_login_Page(request: Request):
    return templates.TemplateResponse("app/login.html", {"request": request, "assets_indent": "../"})

@router.post("/app/login.html")
async def login_for_access_token(request: Request):
    user = await authenticate_user(request)
    # print(user)
    # if not user:
    print(user)
    return RedirectResponse(url = f'../app/index.html?ID={user.ID}', status_code=status.HTTP_302_FOUND)

    # return templates.TemplateResponse("app/index.html", {"request": request, "response" : "error"})
    # else:
    #     print('---------------------')
    #     return templates.TemplateResponse(f"app/index.html", {"request": request})

