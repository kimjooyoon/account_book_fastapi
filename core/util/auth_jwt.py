import bcrypt
import jwt
import datetime

secretKey = 'secret_key!'


def createHashPassword(pw):
    pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return pw


def pwcheck(dest, hashed):
    dest_en = dest.encode('utf-8')
    hashed_en = hashed.encode('utf-8')
    return bcrypt.checkpw(dest_en, hashed_en)


def createToken(id, email):
    exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=300)
    return {'token': jwt.encode({'user_id': id, 'email': email, 'exp': exp}, secretKey)}


def verify(token):
    try:
        jwt.decode(token, secretKey, algorithms='HS256')
    except jwt.ExpiredSignatureError:
        return status.HTTP_401_UNAUTHORIZED
    except jwt.InvalidTokenError:
        return status.HTTP_401_UNAUTHORIZED
    else:
        return True


def decode(token):
    return jwt.decode(token, secretKey, algorithms='HS256', verify=verify(token))
