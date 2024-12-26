from fastapi import APIRouter, Body, FastAPI, File, HTTPException, UploadFile

router = APIRouter()


@router.get("/geometry/hello/", tags=["geometry"], summary="hello geometry.")
async def get_hello():
    return "geometry works OK!"


@router.post("/geometry/square_area/", tags=["geometry", "tool"], summary="Calculate the area of a square.")
def calculate_square_area(side: float):
    if side <= 0:
        raise HTTPException(status_code=400, detail="Side must be a positive number")
    area = side**2
    return area


@router.post("/geometry/triangle_area/", tags=["geometry", "tool"], summary="Calculate the area of a triangle.")
def calculate_triangle_area(base: float, height: float):
    if base <= 0 or height <= 0:
        raise HTTPException(status_code=400, detail="Base and height must be positive numbers")
    area = 0.5 * base * height
    return area


@router.post("/geometry/rectangle_area/", tags=["geometry", "tool"], summary="Calculate the area of a rectangle.")
def calculate_rectangle_area(length: float, width: float):
    if length <= 0 or width <= 0:
        raise HTTPException(status_code=400, detail="Length and width must be positive numbers")
    area = length * width
    return area
