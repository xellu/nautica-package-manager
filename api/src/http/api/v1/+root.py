from napi.http import HTTP, Reply

@HTTP.GET()
async def ping():
    return Reply()