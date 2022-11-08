import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_PATH = ROOT / "app"
PIPELINE_PATH = ROOT / "pipeline"

sys.path += [ROOT.__str__(), APP_PATH.__str__(), PIPELINE_PATH.__str__()]

from app.api import api_router
from fastapi import APIRouter, FastAPI


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

