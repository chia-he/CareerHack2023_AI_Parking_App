from controller.utils import persister
from passlib.context import CryptContext
import uuid

async def insert_VIP(vip_info):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    id = f'VIP_{str(uuid.uuid4()).replace("-","")}'
    print(id)
    cmd_text = f"\
        insert into Parking.VIP (VIP_ID, VIP_NAME, VIP_COMPANY, VIP_USERNAME, VIP_PASSWORD, VIP_EMAIL)\
        values (:VIP_ID, :VIP_NAME, :VIP_COMPANY, :VIP_USERNAME, :VIP_PASSWORD, :VIP_EMAIL)"
    persister.executeNoneQuery(cmd_text,{
        "VIP_ID": id,
        "VIP_NAME" : vip_info.get("NAME"),
        "VIP_COMPANY" : vip_info.get("COMPANY"),
        "VIP_USERNAME":  vip_info.get('USERNAME'),
        "VIP_PASSWORD": pwd_context.hash(vip_info.get('PASSWORD')),
        "VIP_EMAIL": vip_info.get('EMAIL')
    })
    return {"msg": "success", "response":id}

async def get_VIP_by_VI_USERNAME_and_VI_PASSWORD(VI_USERNAME):
    names = ['ID', 'NAME', 'COMPANY', 'USERNAME', 'PASSWORD', 'EMAIL']
    cmd_text = f"\
        select VIP_ID as ID, VIP_NAME as NAME, VIP_COMPANY as COMPANY,\
            VIP_USERNAME as USERNAME, VIP_PASSWORD as PASSWORD, VIP_EMAIL as EMAIL\
        from VIP\
        where VIP_USERNAME=:VIP_USERNAME\
    "
    result = persister.execute(cmd_text, {
        "VIP_USERNAME": VI_USERNAME
    })
    result = persister._list2dict(result, names)

    return {"msg": "success", "response":result}