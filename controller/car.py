from controller.utils import persister

def insert_CAR(ID, CA_LICENSE):
    cmd_text = f"\
        insert into Parking.CAR (CA_ID, CA_OWNERID, CA_LICENSE)\
        values (CONCAT('CA_' , REPLACE(UUID(),'-', '')), :CA_OWNERID, :CA_LICENSE)"
    persister.executeNoneQuery(cmd_text,{
        "CA_OWNERID" : ID,
        "CA_LICENSE" : CA_LICENSE
    })
    return {"msg": "success", "response":[]}


async def get_CAR_by_ID(ID):
    names = ['CA_LICENSE']
    print(ID)
    cmd_text = f"\
        select {','.join(names)} from Parking.CAR where CA_OWNERID=:CA_OWNERID"
    result = persister.execute(cmd_text, {
        "CA_OWNERID": ID
    })
    result = persister._list2dict(result, names)

    return {"msg": "success", "response": result}