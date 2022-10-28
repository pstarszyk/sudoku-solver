from fastapi import APIRouter, FastAPI
from api import api_router


app = FastAPI(
    title="sudoku-solver"
)

root_router = APIRouter()


@root_router.get("/")
def root():
    return {"message": "Welcome to the sudoku-solver app"}


app.include_router(api_router)
app.include_router(root_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)

