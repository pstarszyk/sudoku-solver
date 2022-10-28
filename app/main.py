from fastapi import APIRouter, FastAPI, Request
from api import api_router


app = FastAPI(
    title="test"
)

root_router = APIRouter()


@root_router.get("/")
def root():
    return {"message": "Hello World"}


app.include_router(api_router)
app.include_router(root_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)

