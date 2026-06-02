from napi.http import HTTP, Reply

@HTTP.GET()
def ping():
    return Reply()