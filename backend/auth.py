import bcrypt
from backend import exceptions

def hash_password(password: str) -> str:
    if password == "":
        raise exceptions.EmptyPasswordError
    else:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

def verify_password(password, hashed_password) -> bool:
    if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
        print("The password is correct!")
        return True
    else:
        print("The password is incorrect!")
        return False