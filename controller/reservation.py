from controller.utils import persister

def insert_RESERVATION(re_info, ID, PS_ID, LICENSE):
    Date = re_info.get('reservationDate')
    StartTime = re_info.get('reservationStartTime')
    EndTime = re_info.get('reservationEndTime')
    
    cmd_text = f"\
        insert into Parking.RESERVATIONS (RE_ID, RE_STVIPID, RE_PLID, RE_PSID, RE_VISITING_STARTTIME, RE_VISITING_ENDTIME, RE_LICENSE)\
        values (CONCAT('RE_' , REPLACE(UUID(),'-', '')), :RE_STVIPID, :RE_PLID, :RE_PSID, :RE_VISITING_STARTTIME, :RE_VISITING_ENDTIME, :RE_LICENSE)"
    persister.executeNoneQuery(cmd_text,{
        "RE_STVIPID":ID,
        "RE_PLID" : re_info.get("PL_ID"),
        "RE_PSID" : PS_ID,
        "RE_VISITING_STARTTIME" : f'{Date} {StartTime}',
        "RE_VISITING_ENDTIME":  f'{Date} {EndTime}',
        "RE_LICENSE": LICENSE,
    })
    return {"msg": "success", "response":id}

async def get_all_PARK_HISTORY_by_RE_STVIPID(RE_STVIPID):
    names = ['RE_PLID', 'RE_VISITING_STARTTIME', 'RE_VISITING_ENDTIME', 'RE_LICENSE', 'PS_CODE']
    cmd_text = f"\
        select {','.join(names)}\
        FROM RESERVATIONS\
        inner join PARKING_SPACES on PS_ID=RE_PSID\
        WHERE RE_STVIPID = :RE_STVIPID"
        
    result = persister.execute(cmd_text,{"RE_STVIPID" : RE_STVIPID})    
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}