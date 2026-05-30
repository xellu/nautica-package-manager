from nautica import Services
from nautica.ext.Util import hashStr
from napi.http import Error

import secrets

def UserTemplate():
    return {
        "userId": f"usr_{secrets.token_hex(16)}",
        "username": None,
        "password": None
    }

class User:
    def __init__(self, _id: str = None, _user: dict = None):
        self._id = _id or _user["userId"]
        
        self._user = _user or Services["MongoDB"]("napm_users").find_one({"userId": _id})
        if not self._user:
            raise Error(500, "Account not found", details={"exception": f"Profile with id '{_id}' does not exist"})
    
    @staticmethod
    def create(username, password):
        existing = Services["MongoDB"]("napm_users").find_one({"username": username})
        if existing:
            raise Error(409, "Username already taken")
        
        u = UserTemplate()
        u["username"] = username
        u["password"] = hashStr(f"{u['userId']}${password}")
        
        Services["MongoDB"]("napm_users").insert_one(u)
        return User(u["userId"])
    
    @staticmethod
    def getByUsername(username: str):
        return User(_user=Services["MongoDB"]("napm_users").find_one({"username": username.lower()}))
    
    def verify(self, password: str) -> bool:
        return self._user["password"] == hashStr(f"{self._id}${password}")
    
    def __getitem__(self, key):
        return self._user.get(key)
    
    def __setitem__(self, key, value):
        self._user[key] = value
        Services["MongoDB"]("napm_users").update_one({"userId": self._id}, {"$set": {key: value}})
        