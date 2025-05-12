from pydantic import BaseModel

class SessionData(BaseModel):
    id: int
    username: str