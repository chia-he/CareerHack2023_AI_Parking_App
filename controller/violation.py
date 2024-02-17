
from controller.utils import persister
from controller.utils import email

async def send_email_by_license(license):
    names = ["email"]
    cmd_text = f"\
        select\
            case \
                when ST_EMAIL IS NOT NULL then ST_EMAIL \
                else VIP_EMAIL\
            end as 'email'\
        from Parking.PARK\
        inner join Parking.CAR on PA_LICENSE = CA_LICENSE\
        left join Parking.STAFF on ST_ID = CA_OWNERID\
        left join Parking.VIP on VIP_ID = CA_OWNERID\
        where PA_LICENSE = :PA_LICENSE"
    result = persister.execute(cmd_text, {'PA_LICENSE': license})
    r = persister._list2dict(result, names)
    if len(r) == 0:
        print(r[0])
        return {"msg": "error"}
    else:
        print(r[0]['email'])
        email.SendEmailTo(r[0]['email'])
    return {"msg": "success", "response":r}


async def get_all_violation_times_ph_license():
    names = ["PH_LICENSE, NUM_OF_VIOLATION"]
    cmd_text = f"\
        SELECT PH_LICENSE, COUNT(PH_LICENSE) AS NUM_OF_VIOLATION FROM Parking.VIOLATION\
        INNER JOIN Parking.PARK_HISTORY ON VI_PHID =PH_ID\
        group by PH_LICENSE\
        order by NUM_OF_VIOLATION DESC"
    result = persister.execute(cmd_text)
    r = persister._list2dict(result, names)

    return {"msg": "success", "response":r}

def get_total_VIOLATION():
    names = ['total_violation']
    cmd_text = f"select count( * ) as total_violation from Parking.VIOLATION"
    result = persister.execute(cmd_text)    
    result = persister._list2dict(result, names)
    return {"msg": "success", "response":result}


