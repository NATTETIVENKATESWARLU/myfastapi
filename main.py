from fastapi import FastAPI,HTTPException

app = FastAPI()

brands =[
    {"id": 1, "name": "Brand A"},
    {"id": 2, "name": "Brand B"},
    {"id": 3, "name": "Brand C"},
    {"id": 4, "name": "Brand D"},
    {"id": 5, "name": "Brand E"},
    {"id": 6, "name": "Brand F"},
    {"id": 7, "name": "Brand G"},
    {"id": 8, "name": "Brand H"},
    {"id": 9, "name": "Brand I"},
    {"id": 10, "name": "Brand J"},
    {"id": 11, "name": "Brand K"},
    {"id": 12, "name": "Brand L"},
    {"id": 13, "name": "Brand M"},
    {"id": 14, "name": "Brand N"},
    {"id": 15, "name": "Brand O"},
    {"id": 16, "name": "Brand P"},
    {"id": 17, "name": "Brand Q"},
    {"id": 18, "name": "Brand R"},
    {"id": 19, "name": "Brand S"},
    {"id": 20, "name": "Brand T"}
]


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("about/")
async def read_about() -> str:
    return "This is the about page."


@app.get("/brands/")
async def read_brands() -> list[dict]:
    return brands


@app.get("/brands/{brand_id}")
async def read_brand(brand_id:int):
    brand=next((b for b in brands if b["id"] == brand_id), None)
    if brand is None:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


#query parameters
@app.get("/brands/search/")
async def search_brands(limit:int, offset: int):
    return f"Limit: {limit}, Offset: {offset}"