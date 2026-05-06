from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")


def hash_password(password):
    return pwd_context.hash(password)

def unhash_password(plain_password,password):
    return pwd_context.verify(plain_password,password)