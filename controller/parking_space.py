
from controller.utils import persister


def Insert_PARKING_SPACES():
    cmd_text = f"insert into Parking.PARKING_SPACES (PS_ID, PS_PLID, PS_CODE, PS_TYPE) values"
        
    values = []
    for pl, pl_name in zip(['PL_00001','PL_00002','PL_00003','PL_00004'], ['A','B','C','D']):
        for ps in range(0,100):
            values.append(
                f"(CONCAT('PS_' , REPLACE(UUID(),'-', '')), '{pl}', CONCAT('{pl_name}', LPAD({ps}, 3, '0')), 0)"
            )

    cmd_text += ','.join(values) + ';'
    # print(cmd_text)
    persister.executeNoneQuery(cmd_text,{})
    return {"msg": "success"}

async def get_PARKING_SPACES_info_by_PS_CODE(PS_CODE):
    names = ['PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER', 'PS_ID', 'PS_CODE', 'PS_TYPE']

    cmd_text = f"\
        select {','.join(names)}\
        from Parking.PARKING_SPACES \
        inner join Parking.PARKING_LOT on PS_PLID = PL_ID \
        where PS_CODE = :PS_CODE"
    result = persister.execute(cmd_text,{"PS_CODE" : PS_CODE})
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

async def get_PARK_info_by_PS_CODE(PS_CODE):
    names = ['PA_ID', 'PA_PLID', 'PA_PSID', 'PA_LICENSE', 'PA_IMAGE', 'PA_CREATEDATE' , 'PS_ID' , 'PS_PLID' , 'PS_CODE' , 'PS_TYPE']

    cmd_text = f"\
        select {','.join(names)}\
        from Parking.PARK \
        inner join Parking.PARKING_SPACES on PA_PSID = PS_ID \
        where PS_CODE = :PS_CODE"
    result = persister.execute(cmd_text,{"PS_CODE" : PS_CODE})
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}

async def get_PARKING_LOT_info_by_PL_ID(PL_ID):
    names = ['PL_ID', 'PL_NAME', 'PL_SPACE_NUMBER']
    special_names = ['PARK_OCCUPY_NUMBER', 'EMPTY_SPACE_NUMBER']
    cmd_text = f"\
        SELECT {','.join(names)},\
        case \
            when PARK_OCCUPY_NUMBER IS NULL THEN 0\
            else PARK_OCCUPY_NUMBER\
        END AS PARK_OCCUPY_NUMBER,\
        case \
            when PARK_OCCUPY_NUMBER IS NULL THEN PL_SPACE_NUMBER\
            ELSE (PL_SPACE_NUMBER - PARK_OCCUPY_NUMBER)\
        END AS EMPTY_SPACE_NUMBER\
        FROM PARKING_LOT\
        LEFT JOIN (\
            SELECT PA_PLID, COUNT(PA_ID) AS PARK_OCCUPY_NUMBER\
            FROM PARK\
            GROUP BY PA_PLID\
        ) AS PARK_OCCUPY ON PARK_OCCUPY.PA_PLID = PL_ID\
        WHERE PL_ID = :PL_ID\
        "
    result = persister.execute(cmd_text,{"PL_ID" : PL_ID})
    result = persister._list2dict(result, names+special_names)
    return {"msg": "success", "response":result}