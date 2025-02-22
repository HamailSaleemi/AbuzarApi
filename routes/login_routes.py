from fastapi import APIRouter, HTTPException
from DATABASE.connection import SQL_CONN

# Create an APIRouter instance
router = APIRouter()

@router.get("/")
def login(username: str, password: str):
    try:
        query = "SELECT UserCode, username FROM Users WHERE username = ? AND password = ?"
        params = (username, password)
        result = SQL_CONN.execute_query(query, params)

        if not result:
            raise HTTPException(status_code=404, detail="User not found")

        # Convert result to a list of dictionaries
        users = [{"id": row[0], "username": row[1]} for row in result]


        return {"status": "success", "users": users}

    except Exception as e:
        return {"status": "error", "message": str(e)}
