from model.security_guard import Security_Guard

async def get_security_guard():
    return {"msg":"Hello Router1"}

async def login(sg_info: Security_Guard):
    print(sg_info.username)
    print(sg_info.password)
    return {"msg":"Hello Router1"}

async def logout():
    
    
    return {"msg":"Hello Router1"}