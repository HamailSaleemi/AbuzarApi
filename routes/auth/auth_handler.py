import time
from typing import Dict
from fastapi import HTTPException, status, Depends
import jwt
from decouple import config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()

def sign_jwt(user_id: int, user_name: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "user_name":user_name,
        "expires": time.time() + 2 * (60 * 60)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token
def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token = credentials.credentials
        print(token)
        data = decode_jwt(token)
        print(data)
        print()
        if data['expires'] > time.time():
            return {'user_id':data['user_id'], 'user_name':data['user_name']}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )
    except Exception as E:
        print(E)
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail="Looks Like your session has been expired kindly Login"
        )
