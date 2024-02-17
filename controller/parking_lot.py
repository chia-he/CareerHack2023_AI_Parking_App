from controller.utils import persister

async def get_all_PARKING_LOT_info():
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
        "
    result = persister.execute(cmd_text)
    result = persister._list2dict(result, names+special_names)
    return {"msg": "success", "response":result}