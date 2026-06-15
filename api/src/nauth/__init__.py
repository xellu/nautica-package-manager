from nautica import Services
from plugins.auth import NAuth, NAuthSession
from src.lib.User import User

Auth: NAuth = Services.get("NAuth")
# Usage:
# from src.nauth import Auth
# @Auth.Protect() <- on a route you want protected by auth

# Define a profile getter
def profile_getter(session: NAuthSession):
    return User(session.refId)

# Configure the Auth
Auth.Configure() \
    .setProfileGetter(profile_getter) \
    .addCookieKey("session") \
    .addHeaderKey("Authorization")