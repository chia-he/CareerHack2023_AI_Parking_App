import random

from fastapi import APIRouter, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from model.entry_record import Enter_Record
from model.park import Park
from model.security_guard import Security_Guard
from controller import entry_record, parking_space, park, security_guard, parking_lot, staff, vip, violation
from controller.utils import email
from router import login_api

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/webapi/get_entry_record/{ER_PLID}", tags=['查詢場內所有entry_record'])
async def get_entry_record_by_ER_PLID(ER_PLID) -> dict:
    return await entry_record.get_ENTRY_RECORD_by_ER_PLID(ER_PLID)

# @router.get("/webapi/{PH_ID}", tags=['查詢場內所有parking_record'])
# async def get_parking_record_by_PH_ID(PH_ID) -> dict:
#     return await parking_history.get_ENTRY_RECORD_by_PH_ID(PH_ID)

@router.post("/webapi/insert_entry_record", tags=['新增一筆entry_record'])
def insert_entry_record(er_info:Enter_Record) -> dict:
    return entry_record.insert_ENTRY_RECORD(er_info)

@router.post("/webapi/insert_park", tags=['新增一筆park'])
def insert_park(pa_info:Park) -> dict:
    return park.insert_PARK(pa_info)

@router.post("/webapi/insert_parking_space", tags=['插入多筆 parking_space data'])
def insert_parking_space() -> dict:
    return parking_space.Insert_PARKING_SPACES()

@router.put("/webapi/update_ENTRY_RECORD_exit_time_by_ER_LICENSE/{ER_LICENSE}/{ER_EXIT_TIME}", tags=["修改entry_record 離開時間"])
def update_ENTRY_RECORD_exit_time_by_ER_LICENSE(ER_LICENSE, ER_EXIT_TIME) -> dict:
    return entry_record.update_ENTRY_RECORD_exit_time_by_ER_LICENSE(ER_LICENSE, ER_EXIT_TIME)

@router.post("/webapi/send_email_by_license/{license}", tags=['送信'])
async def send_email_by_license(license):
    return await violation.send_email_by_license(license)

@router.post("/webapi/send_email_for_demo", tags=['送信'])
async def send_email_for_demo(request: Request, url="", PS_CODE="", PL_ID=""):

    email.SendEmailTo("bjes940125@gmail.com")
    print(PS_CODE)
    print(PL_ID)
    if PS_CODE !="":
        return RedirectResponse(f"../web/{url}?PS_CODE={PS_CODE}", status_code=status.HTTP_302_FOUND)
    elif PL_ID!="":
        return RedirectResponse(f"../web/{url}?PL_ID={PL_ID}", status_code=status.HTTP_302_FOUND)
    else:
        return RedirectResponse(f"../web/{url}", status_code=status.HTTP_302_FOUND)
@router.get("/web/url/{HTMLString}", tags=['Other Page'])
async def other_Page(request: Request, HTMLString: str):
    print(HTMLString)
    return templates.TemplateResponse("web/" + HTMLString, {"request": request, "assets_indent": "../../"})

@router.get("/web/index.html", tags=['Other Page'])
async def index_Page(request: Request):

    result = {
        "request": request, 
        "assets_indent": "../", 
        "parking_empty_space": {'PL_00001':await parking_space.get_PARKING_LOT_info_by_PL_ID('PL_00001'),
            'PL_00002':await parking_space.get_PARKING_LOT_info_by_PL_ID('PL_00002'), 
            'PL_00003':await parking_space.get_PARKING_LOT_info_by_PL_ID('PL_00003'), 
            'PL_00004':await parking_space.get_PARKING_LOT_info_by_PL_ID('PL_00004')},
        "park_history": park.get_all_PARK_HISTORY(),
        "violation": violation.get_total_VIOLATION()
    }
    
    print("web: index.html")
    print(result)

    return templates.TemplateResponse("web/index.html", result)

@router.get("/web/parking_lot_info.html", tags=['Other Page'])
async def parking_lot_info_Page(request: Request, PL_ID=""):

    if PL_ID != "":
        temp1 = await parking_space.get_PARKING_LOT_info_by_PL_ID(PL_ID)
        temp2 = park.get_all_PARK_HISTORY_by_PL_ID(PL_ID)
        temp3 = await park.get_all_PARKING_SPACES_STATE(PL_ID)
    else:
        temp1, temp2, temp3 = [], [], []
        
    result = {
        "request": request, 
        "assets_indent": "../", 
        "parking_lot": temp1,
        "park_history": temp2,
        "parking_space_state": temp3
    }

    print("web: parking_lot_info.html")
    print(result)

    return templates.TemplateResponse("web/parking_lot_info.html", result)

@router.get("/web/parking_space_info.html", tags=['Other Page'])
async def parking_space_Page(request: Request, PS_CODE=""):

    result = {
        "request": request, 
        "assets_indent": "../", 
        "parking_space_history": await parking_space.get_PARK_info_by_PS_CODE(PS_CODE) if PS_CODE != "" else []
    }

    print("web: parking_space.html")
    print(result)

    return templates.TemplateResponse("web/parking_space_info.html", result)

@router.get("/web/parking_license_info.html", tags=['Other Page'])
async def parking_license_Page(request: Request, PH_LICENSE=""):

    result = {
        "request": request, 
        "assets_indent": "../", 
        "parking_license_history": await park.get_PARKING_SPACES_HISTORY_info_by_PH_LICENSE(PH_LICENSE) if PH_LICENSE != "" else []
    }

    print("web: parking_license_info.html")
    print(result)

    return templates.TemplateResponse("web/parking_license_info.html", result)

@router.get("/web/blacklist.html", tags=['Other Page'])
async def blacklist_Page(request: Request):

    result = {
        "request": request, 
        "assets_indent": "../", 
        "blacklist": [{'PL_ID': 'PL_00001', 'PL_NAME': 'A', 'PL_SPACE_NUMBER': 100, 'PARK_OCCUPY_NUMBER': 26, 'EMPTY_SPACE_NUMBER': 74} for i in range(20)]
    }

    print("web: blacklist.html")
    print(result)

    return templates.TemplateResponse("web/blacklist.html", result)