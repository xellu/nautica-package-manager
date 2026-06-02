from napi.http import HTTP, Context, Reply, Require, Error
from src.nauth import Auth

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