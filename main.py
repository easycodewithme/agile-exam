from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/status")
async def get_status():
    return {"status": "ok"}


@app.get("/sum")
async def get_sum(a: float, b: float):
    try:
        result = a + b
    except TypeError:
        raise HTTPException(status_code=400, detail="Invalid parameters")
    return {"a": a, "b": b, "sum": result}
