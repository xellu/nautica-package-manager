from napi.http import HTTP, Context, Reply, Error, Require, StatusCodes
from nautica.ext.Util import hashStr

from src.lib.User import User
from src.nauth import Auth

@HTTP.POST()
@HTTP.Require(
    body = {"username": str, "password": str}
)
@Auth.Protect()
def login(ctx: Context):
    return ctx.body["username"]