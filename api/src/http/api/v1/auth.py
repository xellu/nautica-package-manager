from napi.http import HTTP, Context, Reply, Error, Require, StatusCodes, StreamingResponse
from nautica.ext.Util import hashStr, randomStr
from nautica import Services, Scheduler

from src.lib.User import User
from src.nauth import Auth

import io
import time
import random
from captcha.image import ImageCaptcha

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
        .SetCookie("session").value(session.sessionId)
    if ctx.body.get("rememberMe"):
        r.maxAge(7 * 24 * 60 * 60)
        
    return r.build()

@HTTP.POST()
@HTTP.Require(
    body = {"username": str, "password": str, "captchaId": str, "captchaSolution": str}
)
async def register(ctx: Context): 
    if len(ctx.body["username"]) > 40: raise Error(400, "Username too long", details="40 characters maximum")
    if len(ctx.body["username"]) < 3: raise Error(400, "Username too short", details="3 characters minimum")
    if len(ctx.body["password"]) < 8: raise Error(400, "Password too short", details="8 characters minium")
    
    #check captcha
    captcha = Services["MongoDB"]("captchas").find_one({"captchaId": ctx.body["captchaId"]})
    if not captcha:
        raise Error(StatusCodes.NOT_FOUND, "Captcha not found")
    
    if captcha["solution"].lower() != ctx.body["captchaSolution"].lower():
        raise Error(StatusCodes.BAD_REQUEST, "Incorrect captcha solution")
    
    Services["MongoDB"]("captchas").delete_one({"captchaId": ctx.body["captchaId"]}) #clear captcha
    
    user = User.create(
        ctx.body["username"],
        ctx.body["password"]
    )
    remember = ctx.body.get("rememberMe")
    
    session = Auth.createSession(user._id, expire = time.time() + 24 * 60 * 60 * (7 if remember else 1)) #1 week session
    
    r = Reply(session=session.sessionId) \
        .SetCookie("session").value(session.sessionId)

    if remember:
        r.maxAge(7 * 24 * 60 * 60)
        
    return r.build()

@HTTP.GET()
async def captcha(ctx: Context):    
    captchaId = f"cpt_{hashStr(randomStr(32))}"
    solution = "".join(random.choices("ABCDEFGHJKLMNPQRSTUVWXYZ23456789", k=6))
    
    #create captcha image
    image = ImageCaptcha()
    
    captcha_img = image.generate_image(
        solution,
        fg_color = (174, 216, 255),
        bg_color = (20, 22, 42)
    )

    #write to buffer, to avoid saving    
    buffer = io.BytesIO()
    captcha_img.save(buffer, format="PNG")
    buffer.seek(0)
    
    #store to mongo
    Services["MongoDB"]("captchas").insert_one({
        "captchaId": captchaId,
        "solution": solution,
        "expire": time.time() + 5 * 60
    })
    
    #schedule clean up
    def clean_up():
        Services["MongoDB"]("captchas").delete_many({"expire": {"$lt": time.time()}})
    
    Scheduler.RunIn(clean_up, 5*60) #in 5 minutes
    
    return StreamingResponse(buffer, media_type="image/png", headers={
        "n-captcha-id": captchaId
    })
    

@HTTP.GET()
@Auth.Protect()
async def me(ctx: Context):
    return ctx.profile.toDict()