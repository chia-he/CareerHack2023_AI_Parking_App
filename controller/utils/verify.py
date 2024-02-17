from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, Request

from controller import staff, vip, user

class Verify:
    def __init__(self):
        pass
        
    async def get_current_user(self, token: str):
        pass

    async def check_login(self, request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
        print(form_data.username)
        form = await request.form()
        
        username = form_data.username
        password = form_data.password
        identify = form.get('identify')

        if identify == 'staff':
            result = await staff.get_STAFF_by_ST_USERNAME_and_ST_PASSWORD(username, password)
            print(result)
        elif identify == 'vip':
            result = await vip.get_VIP_by_VI_USERNAME_and_VI_PASSWORD(username, password)
        
        if len(result) == 0:
            return {'msg':'success', 'response':'error'}
        else:
            print(result["response"][0])
            user = user.User(**result["response"][0])