import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
APP_PATH = ROOT / "app"
PIPELINE_PATH = ROOT / "pipeline"

sys.path += [ROOT.__str__(), APP_PATH.__str__(), PIPELINE_PATH.__str__()]

from pipeline.image_transform import extract_array
from pipeline.integer_program import solve_board
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from typing import List, Any
from PIL import Image
import numpy as np
import io

app = FastAPI(title="sudoku-solver")


@app.get("/solve")
async def main():
    content = """
        <body>
        <div>
        <form action="/solve" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple="multiple" accept=".png, .jpg, .jpeg">
        <input type="submit">
        </form>
        </div>
        </body>
    """
    return HTMLResponse(content=content)


@app.post("/solve")
async def solve(files: List[UploadFile] = File(...)) -> Any:
    for file in files:
        contents = await file.read()
        image = np.array(Image.open(io.BytesIO(contents)))
        board = extract_array(image=image)
        solution = solve_board(board=board)
    return {"result": solution}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)
