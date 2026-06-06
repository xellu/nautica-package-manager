from nautica import Services, Logger
from nautica.models.Http import AttachedFile
from src.lib.User import User

import re
import time
from copy import deepcopy

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
PACKAGE_NAME = re.compile(r"^(?!.*\.\.)(?![.-])[a-z0-9._-]+(?<![.-])$")

def PackageTemplate():
    return {
        "name": "",
        "versions": [], #PackageVersion
        "installs": 0,

        "displayName": "",
        "brief": "", #short description

        "owner": "", #user id
        "maintainers": [], #list of user ids
    }

def PackageVersion():
    return {
        "id": "0.0.0",
        "file": "", #link to package.zip
        "hash": "",
        "author": "", #user id
        "createdAt": time.time()
    }

class Package:
    def __init__(self, name):
        self.name = name
        
        self._data = Services["MongoDB"]("packages").find_one({"name": self.name}) or {}

        
    def exists(self) -> bool:
        return bool(self._data)
    
    def create(self, owner: User) -> tuple[bool, str]:
        if self.exists(): return False, "Package already exists"
        if not PACKAGE_NAME.match(self.name): return False, "Invalid package name"
        if len(self.name) > 40: return False, "Package name too long"
        if len(self.name) < 3: return False, "Package name too short"
        
        p = PackageTemplate()
        p["name"] = self.name
        p["displayName"] = self.name
        p["owner"] = owner._id
        
        self._data = p
        Services["MongoDB"]("packages").insert_one(p)
        return True, ""
    
    async def addVersion(self, author: User, versionId: str, zipBytes: bytes) -> tuple[bool, str]:
        #perms
        if not self.canEdit(author):
            return False, "Insufficient permissions"
        #version format
        if not SEMVER.match(versionId):
            return False, "Invalid version format. Use semantic versioning: https://semver.org/"
        #version existence
        for v in self._data.get("versions", []):
            if v.get("id") == versionId:
                return False, "Version already exists"
        
        #save file
        filename = f"static/{self.name}-{versionId}-{author._id}.zip"
        with open(filename, "wb") as f:
            f.write(zipBytes)
        
        version = PackageVersion()
        version["id"] = versionId
        version["file"] = filename
        version["author"] = author._id
        
        self._data["versions"].append(version)
        Services["MongoDB"]("packages").update_one({"name": self.name}, {"$set": {"versions": self._data["versions"]}})
        
        return True, ""
    
    def latestVersion(self) -> None | dict:
        latest = None
        for version in self._data.get("versions", []):
            if not latest: latest = version
            if version.get("createdAt") > latest.get("createdAt"): latest = version
            
        return latest
            
    def getVersion(self, versionId) -> None | dict:
        for v in self._data.get("versions", []):
            if v.get("id") == versionId: return v
            
             
    #permissions
    def isMaintainer(self, user: User) -> bool:
        return user._id in self._data.get("maintainers", [])
    def isOwner(self, user: User) -> bool:
        return user._id == self._data.get("owner")
    def canEdit(self, user: User) -> bool:
        return self.isMaintainer(user) or self.isOwner(user) 
    
    #bs
    def toDict(self):
        d = deepcopy(self._data)
        d.pop("_id")
        return d