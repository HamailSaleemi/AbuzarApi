from fastapi import APIRouter

# Create an APIRouter instance
router = APIRouter()

# Define routes for login
@router.get("/")
def get_all_users():
    return {"message": "This is login api"}