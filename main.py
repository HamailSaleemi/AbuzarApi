from fastapi import FastAPI
from routes import login_routes, item_router


app = FastAPI()

@app.get("/ping")
def read_root():
    return {"message": "I am alive"}

# App routers included
app.include_router(login_routes.router, prefix="/login", tags=["Login"])
app.include_router(item_router.router, prefix="/item", tags=["Item"])
app.include_router(item_router.router, prefix="/Supplier", tags=["Supplier"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.10.63", port=8001)
