import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(password, hashed_password) -> bool:
    if bcrypt.checkpw(password, hashed_password):
        print("The passowrd is correct!")
        return True
    else:
        print("The password is incorrect!")
        return False

verify_password("test123".encode("utf-8"), hash_password("test123").encode("utf-8"))
