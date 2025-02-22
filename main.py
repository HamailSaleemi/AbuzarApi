from fastapi import FastAPI
from routes import login_routes


app = FastAPI()

@app.get("/ping")
def read_root():
    return {"message": "I am alive"}

# ✅ Just include the router (No `Depends` required)
app.include_router(login_routes.router, prefix="/login", tags=["login"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
