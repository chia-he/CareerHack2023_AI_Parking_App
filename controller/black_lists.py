from controller.utils import persister
from model.black_lists import Black_Lists

def insert_BLACK_LISTS(bl_info:Black_Lists):
    cmd_text = f"\
        insert into Parking.BLACK_LISTS (BL_ID, BL_LICENSE, BL_STARTTIME, BL_ENDTIME)\
        values (CONCAT('BL_' , REPLACE(UUID(),'-', '')), :BL_LICENSE, :BL_STARTTIME, BL_ENDTIME)"

    persister.executeNoneQuery(cmd_text,{
        "BL_LICENSE" : bl_info.BL_LICENSE,
        "BL_STARTTIME" : bl_info.BL_STARTTIME,
        "BL_ENDTIME" : bl_info.BL_ENDTIME,
    })
    return {"msg": "success"}


def get_BLACK_LISTS_by_BL_LICENSE(BL_LICENSE):
    cmd_text = f"\
        select * from Parking.BLACK_LISTS where BL_LICENSE=:BL_LICENSE"

    persister.executeNoneQuery(cmd_text,{
        "BL_LICENSE" : BL_LICENSE
    })
    return {"msg": "success"}