
from model.entry_record import Enter_Record
from controller.utils import persister
from datetime import datetime

async def get_ENTRY_RECORD_by_ER_PLID(ER_PLID: str):
    names = ["ER_ID", "ER_PLID", "ER_LICENSE", "ER_ENTER_TIME", "ER_EXIT_TIME"]
    cmd_text = f"select * from Parking.ENTRY_RECORD where ENTRY_RECORD.ER_PLID = :ER_PLID"
    result = persister.execute(cmd_text, {'ER_PLID': ER_PLID})
    r = persister._list2dict(result, names)
    return {"msg": "success", "response":r}

def insert_ENTRY_RECORD(er_info:Enter_Record):
    cmd_text = f"\
        insert into Parking.ENTRY_RECORD (ER_ID, ER_PLID, ER_LICENSE, ER_ENTER_TIME, ER_IMAGE)\
        values (CONCAT('PL_' , REPLACE(UUID(),'-', '')), :ER_PLID, :ER_LICENSE, :ER_ENTER_TIME, :ER_IMAGE)"
    persister.executeNoneQuery(cmd_text,{
        "ER_PLID" : er_info.ER_PLID,
        "ER_LICENSE" : er_info.ER_LICENSE,
        "ER_ENTER_TIME":  datetime.now().__str__() if er_info.ER_ENTER_TIME is None else er_info.ER_ENTER_TIME,
        "ER_IMAGE": er_info.ER_IMAGE
    })
    return {"msg": "success"}

def update_ENTRY_RECORD_exit_time_by_ER_LICENSE(ER_LICENSE, ER_EXIT_TIME):
    cmd_text = f"\
        update Parking.ENTRY_RECORD \
        set ER_EXIT_TIME = :ER_EXIT_TIME\
        where ER_LICENSE = :ER_LICENSE\
    "
    persister.executeNoneQuery(cmd_text,{
        "ER_EXIT_TIME" : ER_EXIT_TIME,
        "ER_LICENSE"  : ER_LICENSE
    })
    return {"msg": "success"}
