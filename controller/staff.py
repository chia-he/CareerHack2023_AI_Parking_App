from controller.utils import persister
from model.user import User
from passlib.context import CryptContext
import uuid
async def insert_STAFF(st_info):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    id = f'ST_{str(uuid.uuid4()).replace("-","")}'
    cmd_text = f"\
        insert into Parking.STAFF (ST_ID, ST_NAME, ST_NUMBER, ST_USERNAME, ST_PASSWORD, ST_EMAIL)\
        values (:ST_ID, :ST_NAME, :ST_NUMBER, :ST_USERNAME, :ST_PASSWORD, :ST_EMAIL)"
    persister.executeNoneQuery(cmd_text,{
        "ST_ID":id,
        "ST_NAME" : st_info.get("NAME"),
        "ST_NUMBER" : st_info.get("NUMBER"),
        "ST_USERNAME":  st_info.get('USERNAME'),
        "ST_PASSWORD": pwd_context.hash(st_info.get('PASSWORD')),
        "ST_EMAIL": st_info.get('EMAIL')
    })
    return {"msg": "success", "response":id}

async def get_STAFF_by_ST_USERNAME_and_ST_PASSWORD(ST_USERNAME):
    names = ['ID', 'NAME', 'NUMBER', 'USERNAME', 'PASSWORD', 'EMAIL']
    cmd_text = f"\
        select ST_ID as ID, ST_NAME as NAME, ST_NUMBER as NUMBER,\
            ST_USERNAME as USERNAME, ST_PASSWORD as PASSWORD, ST_EMAIL as EMAIL\
        from STAFF\
        where ST_USERNAME=:ST_USERNAME\
    "
    result = persister.execute(cmd_text, {
        "ST_USERNAME": ST_USERNAME
    })
    result = persister._list2dict(result, names)

    return {"msg": "success", "response":result}

async def get_STAFF_by_ST_ID(ST_ID):
    names = ['ID', 'NAME', 'NUMBER', 'USERNAME', 'PASSWORD', 'EMAIL']
    cmd_text = f"\
        select ST_ID as ID, ST_NAME as NAME, ST_NUMBER as NUMBER,\
            ST_USERNAME as USERNAME, ST_PASSWORD as PASSWORD, ST_EMAIL as EMAIL\
        from STAFF\
        where ST_ID=:ST_ID\
    "
    result = persister.execute(cmd_text, {
        "ST_ID": ST_ID
    })
    result = persister._list2dict(result, names)

    return {"msg": "success", "response":result}

async def get_STAFF_HISTORY_by_STID(ST_ID):
    names = ['PL_NAME', 'ER_ENTER_TIME', 'CA_LICENSE']
    cmd_text = f"\
        SELECT {','.join(names)}\
        FROM STAFF\
        inner join CAR ON CA_OWNERID = ST_ID\
        inner join PARK_HISTORY ON PH_LICENSE = CA_LICENSE\
        inner join PARKING_LOT ON PH_PLID = PL_ID\
        inner join ENTRY_RECORD on CA_LICENSE = ER_LICENSE\
        where ST_ID = :ST_ID\
    "
    result = persister.execute(cmd_text, {
        "ST_ID": ST_ID
    })
    result = persister._list2dict(result, names)

    return {"msg": "success", "response":result}