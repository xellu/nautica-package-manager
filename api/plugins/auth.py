from nautica import Service, Config, ConfigBuilder, Logger, Services, Scheduler
from nautica.ext.Util import maybeAwait
from napi.http import Context, HTTP, Error, StatusCodes


import os
import time
import secrets

class NAuthConfig:
    """
    Fluent configuration object for NAuth
    Use to define where to look for session tokens and how to resolve a user profile.
    """

    def __init__(self):
        self.headerSearchFor: set[str] = set()
        self.cookieSearchFor: set[str] = set()
        self.profileGetter: callable | None = None

    def addHeaderKey(self, key: str):
        """Register a request header name to search for a session token."""
        self.headerSearchFor.add(key)
        return self

    def addCookieKey(self, key: str):
        """Register a cookie name to search for a session token."""
        self.cookieSearchFor.add(key)
        return self

    def setProfileGetter(self, func: callable):
        """Set the callable used to resolve a user profile from a session document. Its return value is attached to ctx.profile."""
        self.profileGetter = func
        return self
    
class NAuthSession:
    def __init__(self, sessionId: str = None, refId: str = None, expire: float | None = None):
        """
        :param sessionId: Unique session token; auto-generated if omitted.
        :param refId: Caller-defined reference (e.g. user ID) tied to this session.
        :param expire: Unix timestamp after which the session is invalid; defaults to 1 hour from now.
        """
        self.sessionId = sessionId or secrets.token_hex(32)
        self.refId = refId
        self.expire: float | None = expire

    def toDict(self) -> dict:
        return {"sessionId": self.sessionId, "refId": self.refId, "expire": self.expire}
        

class NAuth(Service):
    def __init__(self):
        super().__init__()
        self.config: NAuthConfig = NAuthConfig()
        
        self.nextClean = 0

    def onInstall(self):
        Config.Update("nautica", ConfigBuilder()
            .add("services.nauth", False, comment="Enable nauth")
            .build()
        )

    def isEnabled(self):
        return Config("nautica")["services.nauth"]

    def onStart(self, registry):
        if not os.path.exists("src/nauth/__init__.py"):
            with open(f"src/nauth/__init__.py", "w") as f: f.write(NAuthPreset)
            
    def onClose(self, reason):
        pass

    def Protect(self):
        """Decorator that gates a route behind session authentication when NAuth is enabled."""
        def decorator(func):
            if self.isEnabled():
                HTTP.Before(func)(self.handleRequest)
            return func
        return decorator

    def Configure(self):
        """Return the mutable NAuthConfig for fluent configuration chaining."""
        return self.config
    
    def createSession(self, refId: str, expire: float | None) -> NAuthSession:
        """
        Create a new session
        
        :refId: A reference ID - use this to define for example user ID
        :expire: When to expire - Timestamp or None to never expire
        """
        s = NAuthSession(refId = refId, expire = expire)
        Services["MongoDB"]("nauth_sessions").insert_one(s.toDict())
        
        return s
        
    def deleteSession(self, sessionId: str):
        """Delete a single session by its session token."""
        Services["MongoDB"]("nauth_sessions").delete_one({"sessionId": sessionId})

    def deleteMany(self, refId: str):
        """Delete all sessions associated with the given refId (e.g. when a user logs out everywhere)."""
        Services["MongoDB"]("nauth_sessions").delete_many({"refId": refId})

    def deleteExpired(self):
        """Deletes all sessions that have already expired."""
        Services["MongoDB"]("nauth_sessions").delete_many({"expire": {"$ne": None, "$lt": time.time()}})
        Logger.info("Deleted expired sessions")

    async def handleRequest(self, ctx: Context):
        sessionId: str | None = None
        
        if time.time() > self.nextClean:
            self.deleteExpired()
            self.nextClean = time.time() + 60 * 60
        
        for key in self.config.headerSearchFor:
            if key in ctx.headers:
                sessionId = ctx.headers[key]
                break
            
        if not sessionId:
            for key in self.config.cookieSearchFor:
                if key in ctx.cookies:
                    sessionId = ctx.cookies[key]
                    break
                
        if not sessionId:
            raise Error(StatusCodes.UNAUTHORIZED, "No session provided", details={
                "exception": "Expected a header or cookie with session, got none"
            })
            
        s = Services["MongoDB"]("nauth_sessions").find_one({"sessionId": sessionId})
        if not s:
            raise Error(StatusCodes.UNAUTHORIZED, "Unknown session")
            
        if s["expire"] and s["expire"] < time.time():
            Services["MongoDB"]("nauth_sessions").delete_one({"sessionId": sessionId})
            raise Error(StatusCodes.UNAUTHORIZED, "Session expired")
        
        if not self.config.profileGetter:
            return
        
        try:
            profile = await maybeAwait(self.config.profileGetter(s))
            setattr(ctx, "profile", profile)
        except Exception as e:
            Logger.trace(e)
            raise Error(StatusCodes.INTERNAL_SERVER_ERROR, "Unable to retrieve profile data", details={
                "exception": str(e)
            })    
    
Service.Export(
    NAuth,
    srcDir="nauth",
    depends_on = ["MongoDB"]
)

NAuthPreset = """
from nautica import Services
from plugins.auth import NAuth, NAuthSession

Auth: NAuth = Services.Get("NAuth")
# Usage:
# from src.nauth import Auth
# @Auth.Protect() <- on a route you want protected by auth

# Define a profile getter
def profile_getter(session: NAuthSession):
    return {
        #define your profile object here
    }
    #output of this function will be available in the request handler as 'ctx.profile' <- this can be anything: dict, user manager, etc.

# Configure the Auth
Auth.Configure() \
    .setProfileGetter(profile_getter) \
    .addCookieKey("session") \
    .addHeaderKey("Authorization")
"""
