from napi.http import HTTP, Context, Reply, Error, Require, StatusCodes
from nautica.ext.Util import hashStr

from src.lib.User import User
from src.nauth import Auth

import time

@HTTP.POST()
@HTTP.Require(
    body = {"username": str, "password": str}
)
async def login(ctx: Context):
    user: User = User.getByUsername(ctx.body["username"])
    
    if not user or not user.verify(ctx.body["password"]):
        raise Error(StatusCodes.UNAUTHORIZED, "Incorrect username or password")
    
    session = Auth.createSession(user._id, expire = time.time() + 24 * 60 * 60 * (7 if "rememberMe" in ctx.body else 1)) #1 week session
    
    r = Reply(session=session.sessionId) \
        .SetCookie("session").value(session.sessionId).httpOnly()

    if ctx.body.get("rememberMe"):
        r.maxAge(7 * 24 * 60 * 60)
        
    return r.build()

@HTTP.POST()
@HTTP.Require(
    body = {"username": str, "password": str}
)
async def register(ctx: Context):
    if len(ctx.body["username"]) > 40: raise Error(400, "Username too long", details="40 characters maximum")
    if len(ctx.body["username"]) < 3: raise Error(400, "Username too short", details="3 characters minimum")
    if len(ctx.body["password"]) < 8: raise Error(400, "Password too short", details="8 characters minium")
    
    user = User.create(
        ctx.body["username"],
        ctx.body["password"]
    )
    
    session = Auth.createSession(user._id, expire = time.time() + 24 * 60 * 60 * (7 if "rememberMe" in ctx.body else 1)) #1 week session
    
    r = Reply(session=session.sessionId) \
        .SetCookie("session").value(session.sessionId).httpOnly()

    if ctx.body.get("rememberMe"):
        r.maxAge(7 * 24 * 60 * 60)
        
    return r.build()

@HTTP.GET()
@Auth.Protect()
async def me(ctx: Context):
    return ctx.profile.toDict()