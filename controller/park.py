
from model.park import Park
from controller.utils import persister
from datetime import datetime


def insert_PARK(pa_info:Park):
    cmd_text = f"\
        insert into Parking.PARK (PA_ID, PA_PLID, PA_PSID, PA_LICENSE, PA_IMAGE)\
        values (CONCAT('PA_' , REPLACE(UUID(),'-', '')), :PA_PLID, :PA_PSID, :PA_LICENSE, :PA_IMAGE)"
    persister.executeNoneQuery(cmd_text,{
        "PA_PLID" : pa_info.PA_PLID,
        "PA_PSID" : pa_info.PA_PSID,
        "PA_LICENSE":  pa_info.PA_LICENSE,
        "PA_IMAGE": pa_info.PA_IMAGE
    })
    return {"msg": "success"}

def get_all_PARK():
    names = ['PA_LICENSE', 'PA_CREATEDATE', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE','PA_IMAGE']
    cmd_text = f"\
        select {','.join(names)}\
        FROM Parking.PARK\
        inner join Parking.PARKING_SPACES ON PA_PSID = PS_ID\
        inner join Parking.PARKING_LOT on PA_PLID = PL_ID"
    result = persister.execute(cmd_text)    
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

def get_all_PARK_HISTORY():
    names = ['PH_LICENSE', 'PH_CREATETIME', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE','PH_IMAGE']
    cmd_text = f"\
        select {','.join(names)}\
        FROM Parking.PARK_HISTORY\
        inner join Parking.PARKING_SPACES ON PH_PSID = PS_ID\
        inner join Parking.PARKING_LOT on PH_PLID = PL_ID"

    result = persister.execute(cmd_text)    
    result = persister._list2dict(result, names)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    return {"msg": "success", "response":result}

def get_all_PARK_HISTORY_by_PL_ID(PL_ID):
    names = ['PH_LICENSE', 'PH_CREATETIME', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE','PH_IMAGE']
    cmd_text = f"\
        select {','.join(names)}\
        FROM Parking.PARK_HISTORY\
        inner join Parking.PARKING_SPACES ON PH_PSID = PS_ID\
        inner join Parking.PARKING_LOT on PH_PLID = PL_ID\
        WHERE PL_ID = :PL_ID"
        
    result = persister.execute(cmd_text,{"PL_ID" : PL_ID})    
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

def get_PARK_HISTORY_by_PH_LICENSE(PH_LICENSE):
    names = ['PH_LICENSE', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE','PH_IMAGE']
    cmd_text = f"\
        select {','.join(names)}\
        FROM Parking.PARK_HISTORY\
        inner join Parking.PARKING_SPACES ON PH_PSID = PS_ID\
        inner join Parking.PARKING_LOT on PH_PLID = PL_ID\
        WHERE PH_LICENSE = :PH_LICENSE"
        
    result = persister.execute(cmd_text,{"PH_LICENSE" : PH_LICENSE})    
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

async def get_all_PARKING_SPACES_STATE(PL_ID):
    names = ['PA_ID', 'PS_ID', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE']

    cmd_text = f"\
        select {','.join(names)}\
        FROM PARK\
        right join PARKING_SPACES ON PA_PSID = PS_ID\
        inner join PARKING_LOT on PL_ID = PS_PLID\
        where PL_ID = :PL_ID"
    result = persister.execute(cmd_text,{"PL_ID" : PL_ID})
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

async def get_PARKING_SPACES_info_by_PA_LICENSE(PA_LICENSE):
    names = ['PA_LICENSE', 'PA_IMAGE', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE']

    cmd_text = f"\
        select {','.join(names)}\
        FROM Parking.PARK\
        inner join Parking.PARKING_SPACES ON PA_PSID = PS_ID\
        inner join Parking.PARKING_LOT on PA_PLID = PL_ID\
        where PA_LICENSE = :PA_LICENSE"
    result = persister.execute(cmd_text,{"PA_LICENSE" : PA_LICENSE})
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

async def get_PARKING_SPACES_HISTORY_info_by_PH_LICENSE(PH_LICENSE):
    names = ['PH_LICENSE', 'PH_IMAGE', 'PH_CREATETIME', 'PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_CODE', 'PS_TYPE']

    cmd_text = f"\
        select {','.join(names)}\
        FROM Parking.PARK_HISTORY\
        inner join Parking.PARKING_SPACES ON PH_PSID = PS_ID\
        inner join Parking.PARKING_LOT on PH_PLID = PL_ID\
        where PH_LICENSE = :PH_LICENSE"
    result = persister.execute(cmd_text,{"PH_LICENSE" : PH_LICENSE})
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

