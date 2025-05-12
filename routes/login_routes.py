from fastapi import APIRouter, HTTPException
from DATABASE.connection import SQL_CONN
from pydantic import BaseModel

# Create an APIRouter instance
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/")
def login(request: LoginRequest):
    # return {"username": request.username, "password": request.password}
    try:
        query = "SELECT UserCode, username FROM Users WHERE username = ? AND password = ?"
        params = (request.username, request.password)
        result = SQL_CONN.execute_query(query, params)
        print('result is ',result)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert result to a list of dictionaries
        users = [{"id": row[0], "username": row[1]} for row in result]
        print('username ', users)

        return {"status": "success", "users": users}

    except Exception as e:
        return {"status": "error", "message": str(e)}
