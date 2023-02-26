from pipeline.image_transform import extract_array
from pipeline.integer_program import solve_board
from pipeline.output_image import generate_content
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import HTMLResponse, Response
from typing import List, Any
from PIL import Image
import numpy as np
import io

api_router = APIRouter()


@api_router.get("/solve")
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


@api_router.post("/solve")
async def solve(files: List[UploadFile] = File(...)) -> Any:
    for file in files:
        input = await file.read()
        image = np.array(Image.open(io.BytesIO(input)))
        board, output = extract_array(image=image)
        solution = solve_board(board=board)
        content = generate_content(board=board,
                                   solution=solution,
                                   output=output)

        content_image = Image.fromarray(content)
        with io.BytesIO() as buffer:
            content_image.save(buffer, format='PNG')
            content_bytes = buffer.getvalue()

    return Response(content=content_bytes, media_type="image/png")
