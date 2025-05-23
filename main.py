from fastapi import FastAPI
from routes import login_routes, item_router, supplier_route


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# allow middleware cores
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with exact origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def read_root():
    return {"message": "I am alive"}

# App routers included
app.include_router(login_routes.router, prefix="/login", tags=["Login"])
app.include_router(item_router.router, prefix="/item", tags=["Item"])
app.include_router(supplier_route.router, prefix="/supplier", tags=["Item"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
