from napi.http import HTTP, Context, Reply, Error, Require, RedirectResponse, FileResponse
from nautica import Logger, Services
from nautica.models.Http import AttachedFile

from src.lib.Package import Package
from src.lib.User import User
from src.nauth import Auth

import io
import os
import math
import tomlkit
from zipfile import  ZipFile

@HTTP.POST()
@HTTP.Require(
    files = {"package": Require.File(Require.File.MB(10))}
)
@Auth.Protect()
async def publish(ctx: Context):
    package: AttachedFile = ctx.files["package"]
    zipBytes = await package.read()
    
    with ZipFile(io.BytesIO(zipBytes), "r") as zf:
        with zf.open("project.n3", "r") as f:
            meta = tomlkit.loads(f.read().decode("utf-8"))
            name = meta.get("name")
            version = meta.get("version")
        
    #validate meta
    if not name:
        raise Error(400, "Malformed project.n3", "No name specified")
    if not version:
        raise Error(400, "Malformed project.n3", "No version specified")
    
    
    p = Package(name)
    if not p.exists(): #create package
        ok, error = p.create(ctx.profile)
        if not ok:
            raise Error(400, error)
                
    ok, error = await p.addVersion(ctx.profile, version, zipBytes)
    if not ok:
        raise Error(400, error)
    
    return Reply(ok=True)

@HTTP.Before(publish)
def before_pub(ctx: Context):
    Logger.dir(ctx)

@HTTP.GET()
@HTTP.Require(
    query = {"package": str}
)
def versions(ctx: Context):
    p = Package(ctx.query["package"])
    if not p.exists():
        raise Error(404, "Package does not exist")
    
    return p.toDict().get("versions")

@HTTP.GET("/page/{package:str}/{version:str}")
def page(ctx: Context, package: str, version: str):
    p = Package(package)
    if not p.exists():
        raise Error(404, "Package does not exist")
    
    page = p.toDict()
    page["readMe"] = "No README available to show."
    
    maintainers = []
    for userId in page.get("maintainers", []):
        try: u = User(userId)
        except: u = {"username": "(INACCESSIBLE)"}
        maintainers.append({"username": u["username"], "id": userId})
    
    page["maintainersExpanded"] = maintainers
    page["ownerExpanded"] = {"username": User(page["owner"])["username"], "id": page["owner"]}
    
    release = p.latestVersion() if version == "latest" else p.getVersion(version)
    if release is None:
        raise Error(404, "Release not found")
    
    try: 
        with ZipFile(release.get("file"), "r") as zf:
            try:
                with zf.open("README.md", "r") as f:
                    page["readMe"] = f.read().decode()
            except:
                pass
    except FileNotFoundError:
        Logger.error(f"Dist file for {version} not found")
        page["readMe"] = "# Error\n> Distributable for this version is missing"
            
    return page

@HTTP.GET("/install/{package:str}/{version:str}")
def install(ctx: Context, package: str, version: str):
    p = Package(package)
    if not p.exists():
        raise Error(404, "Package does not exist")

    ver = p.latestVersion() if version == "latest" else p.getVersion(version)
    if not ver:
        raise Error(404, "Package version does not exist")
    
    p["installs"] = p.get("installs", 0) + 1
    
    if ver.get("file").startswith("static"):
        return FileResponse(path=ver["file"], filename=os.path.basename(ver["file"]))
    
    return RedirectResponse(url=ver.get("file"))

@HTTP.GET()
def featured():
    ps = Services["MongoDB"]("packages").find(
        {},
        {"_id": 0}
    ).sort("installs", -1).limit(10)
    
    return list(ps)

@HTTP.GET()
@HTTP.Require(query={"query": str, "page": int})
def search(ctx: Context):
    query = ctx.query["query"]
    page = abs(ctx.query["page"] - 1)
    limit = 10
    
    filter = {
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"displayName": {"$regex": query, "$options": "i"}},
            {"brief": {"$regex": query, "$options": "i"}},
        ]
    }
    
    result_count = Services["MongoDB"]("packages").count_documents(filter)
    results = Services["MongoDB"]("packages").find(filter, {"_id": 0, "versions": 0}) \
        .sort("installs", -1) \
        .skip(page * limit) \
        .limit(limit)
        
    page_count = math.ceil(result_count / limit)
    
    return Reply(
        results = list(results),
        pageCount = page_count,
        resultCount = result_count
    )