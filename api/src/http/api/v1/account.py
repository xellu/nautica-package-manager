from napi.http import HTTP, Context, Reply, Error
from src.nauth import Auth
from src.lib.Package import Package

from nautica import Services

@HTTP.GET()
@Auth.Protect()
async def packages(ctx: Context):
    ps = Services["MongoDB"]("packages").find({
        "$or": [
            {"owner": ctx.profile._id},
            {"maintainers": ctx.profile._id}
        ]
    })
    out = []
    for p in ps:
        p.pop("_id")
        out.append(p)
        
    return out

@HTTP.POST("/update-package/{package:str}")
@HTTP.Require(body={"brief": str, "displayName": str})
@Auth.Protect()
async def update_package(ctx: Context, package: str):
    p = Package(package)
    if not p.canEdit(ctx.profile):
        raise Error(403, "Insufficient permissions")
    
    brief = ctx.body["brief"]
    displayName = ctx.body["displayName"]
    
    if len(brief) > 300: raise Error(400, "Brief description too long")
    if len(displayName) < 3: raise Error(400, "Display name too short")
    if len(displayName) > 40: raise Error(400, "Display name too long")
    
    p["brief"] = brief
    p["displayName"] = displayName
    
    return Reply()