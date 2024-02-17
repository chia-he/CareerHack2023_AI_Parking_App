from fastapi import APIRouter, Request, Depends
from controller import parking_space, park
from fastapi.templating import Jinja2Templates
from controller import entry_record, parking_space, park, security_guard, parking_lot, staff, vip,car, reservation
from router import login_api
import starlette.status as status
from fastapi.responses import RedirectResponse, HTMLResponse

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/appapi/get_PARKING_SPACES_info_by_PS_CODE/{PS_CODE}", tags=['查詢停車格資訊'])
async def get_PARKING_SPACES_info_by_PS_CODE(PS_CODE) -> dict:
    return await parking_space.get_PARKING_SPACES_info_by_PS_CODE(PS_CODE)

@router.get("/appapi/get_PARKING_SPACES_info_by_PA_LICENSE/{PA_LICENSE}", tags=['查詢車子停在哪裡'])
async def get_PARKING_SPACES_info_by_PA_LICENSE(PA_LICENSE) -> dict:
    print(PA_LICENSE)
    return await park.get_PARKING_SPACES_info_by_PA_LICENSE(PA_LICENSE)

@router.get("/appapi/get_PARKING_LOT_info_by_PL_ID/{PL_ID}", tags=['查詢停車場車格數量'])
async def get_PARKING_LOT_info_by_PL_ID(PL_ID) -> dict:
    return await parking_space.get_PARKING_LOT_info_by_PL_ID(PL_ID)


## App Related


@router.get("/app/url/{HTMLString}", tags=['Other Page'])
async def other_Page(request: Request, HTMLString: str):
    print(HTMLString)
    return templates.TemplateResponse("app/" + HTMLString, {"request": request, "assets_indent": "../../"})

@router.post("/app/register.html", tags=['送出註冊表單'])
async def register_user(request: Request):
    form = await request.form()
    identify = form.get('identity')

    if identify == "staff":
        result = await staff.insert_STAFF(form)
    elif identify == "vip":
        result = await vip.insert_VIP(form)
        
    car.insert_CAR(result['response'], form.get('LICENSE'))
    return RedirectResponse(url = f'../app/login.html', status_code=status.HTTP_302_FOUND)
    # return templates.TemplateResponse("app/login.html", {"request": request})

@router.get("/app/parking_lot_info.html", tags=['Other Page'])
async def parking_lot_info_Page(request: Request, PL_ID="", ST_ID=""):
    print("app: parking_lot_info.html")
    print(ST_ID)
    if PL_ID != "":
        result = await parking_space.get_PARKING_LOT_info_by_PL_ID(PL_ID)
    else:
        result = await parking_lot.get_all_PARKING_LOT_info()
    return templates.TemplateResponse("app/parking_lot_info.html", {"request": request, "assets_indent": "../", "parking_lot": result['response']})

@router.get("/app/reservation.html")
async def get_RESERSERVATIONS(request: Request, ID=""):
    print(ID)
    
    return templates.TemplateResponse("app/reservation.html", {"request": request}) 

@router.post("/app/reservation.html")
async def insert_RESERSERVATIONS_(request: Request, ID=''):
    
    form = await request.form()
    
    park_result = await park.get_all_PARKING_SPACES_STATE(form.get('PL_ID'))
    car_result = await car.get_CAR_by_ID(ID)
    space_result = await reservation.get_all_PARK_HISTORY_by_RE_STVIPID(ID)
    for i in park_result["response"]:
        if i['PA_ID'] is None:
            PS_ID = "PS_c654a1c6a85a11edba854201c0a80002"
            break
    else:
        space_result['response']['PS_CODE'] = '已滿，請另行預約'
        return templates.TemplateResponse("app/reservation.html", {"request": "此廠區已滿", "parking_space":space_result['response']}) 
 
    reservation.insert_RESERVATION(form, ID, PS_ID, car_result["response"][0]["CA_LICENSE"])
    return templates.TemplateResponse("app/reservation.html", {"request": request, "parking_space":space_result['response']}) 

@router.get("/app/index.html", tags=['Other Page'])
async def index_Page(request: Request, ID=""):
    print(request)
    print("index.html")
    if ID:
        result = await reservation.get_all_PARK_HISTORY_by_RE_STVIPID(ID)
        # result2 = await staff.get_STAFF_HISTORY_by_STID(ID)

    else:
        result = {'response':[]}
    return templates.TemplateResponse("app/index.html", {"request": request, "assets_indent": "../", 'history_info':result['response']})

@router.get("/app/forgot_password.html", tags=['Other Page'])
async def forgot_password_Page(request: Request, PA_LICENSE=""):
    # print("forgot_password.html")
    return templates.TemplateResponse("app/forgot_password.html", {"request": request, "assets_indent": "../",})

@router.get("/app/register.html", tags=['Other Page'])
async def register_Page(request: Request, PA_LICENSE=""):
    return templates.TemplateResponse("app/register.html", {"request": request, "assets_indent": "../",})

# @router.get("/app/reservation.html", tags=['Other Page'])
# async def reservation_Page(request: Request, PA_LICENSE=""):
#     return templates.TemplateResponse("app/reservation.html", {"request": request, "assets_indent": "../",})

@router.get("/app/find_vehicle.html", tags=['Other Page'])
async def find_vehicle_Page(request: Request, PA_LICENSE="", ID=""):
    print("app: find_vehicle.html")
    result = await park.get_PARKING_SPACES_info_by_PA_LICENSE(PA_LICENSE)
    print(result)
    return templates.TemplateResponse("app/find_vehicle.html", {"request": request, "assets_indent": "../", "park": result['response']})

@router.get("/app/navigation.html", tags=['Other Page'])
async def navigation_Page(request: Request, PA_LICENSE=""):
    print("app: navigation.html")
    return templates.TemplateResponse("app/navigation.html", {"request": request, "assets_indent": "../"})

@router.get("/app/setting.html", tags=['Other Page'])
async def setting_Page(request: Request, ID=""):
    # if ID:
    #     result = staff.get_STAFF_by_ST_ID(ID)
    # else:
    #     result = {'response':[]}
    result = {'response':[]}
    print("app: setting.html")
    return templates.TemplateResponse("app/setting.html", {"request": request, "assets_indent": "../", 'personal_info':result['response']})