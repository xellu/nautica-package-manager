from napi.http import HTTP, Context, Reply, Error, Require, RedirectResponse, FileResponse
from nautica import Logger
from nautica.models.Http import AttachedFile

from src.lib.Package import Package
from src.lib.User import User
from src.nauth import Auth

import io
import os
import tomlkit
from zipfile import  ZipFile

@HTTP.POST()
@HTTP.Require(
    files = {"package": Require.File(Require.File.MB(10))}
)
@Auth.Protect()
async def publish(ctx: Context):
    print("entry")
    package: AttachedFile = ctx.files["package"]
    
    print("b4 read")
    zipBytes = await package.read()
    with ZipFile(io.BytesIO(zipBytes), "r") as zf:
        with zf.open("project.n3", "r") as f:
            meta = tomlkit.loads(f.read().decode("utf-8"))
            name = meta.get("name")
            version = meta.get("version")
            print(f"UNZIP: {name=}, {version=}")
            # dependsOn = meta.get("dependsOn", []) #not rly needed
            # pyPackages = meta.get("pyPackages", [])
        
    print("after read")
    
    #validate meta
    if not name:
        raise Error(400, "Malformed project.n3", "No name specified")
    if not version:
        raise Error(400, "Malformed project.n3", "No version specified")
    
    print("passed checks")
    
    p = Package(name)
    if not p.exists(): #create package
        ok, error = p.create(ctx.profile)
        if not ok:
            raise Error(400, error)
        
    print("passed duplicates")
        
    ok, error = await p.addVersion(ctx.profile, version, zipBytes)
    print(f"create {ok=} {error=}")
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
    
    with ZipFile(release.get("file"), "r") as zf:
        try:
            with zf.open("README.md", "r") as f:
                page["readMe"] = f.read().decode()
        except:
            pass
        
    return page

@HTTP.GET("/install/{package:str}/{version:str}")
def install(ctx: Context, package: str, version: str):
    p = Package(package)
    if not p.exists():
        raise Error(404, "Package does not exist")

    ver = p.latestVersion() if version == "latest" else p.getVersion(version)
    if not ver:
        raise Error(404, "Package version does not exist")
    
    if ver.get("file").startswith("static"):
        return FileResponse(path=ver["file"], filename=os.path.basename(ver["file"]))
    
    return RedirectResponse(url=ver.get("file"))