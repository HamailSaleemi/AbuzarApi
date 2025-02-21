import SQL  # Ensure SQL.py is in the same directory
from fastapi import FastAPI
from routes import login_routes


conn = SQL.conn
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# Including all routes
app.include_router(login_routes.router, prefix="/login", tags=["login"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)