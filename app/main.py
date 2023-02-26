import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(ROOT.__str__())

from app.api import api_router
from fastapi import APIRouter, FastAPI


app = FastAPI(
    title="sudoku-solver"
)

root_router = APIRouter()

app.include_router(api_router)
app.include_router(root_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)

