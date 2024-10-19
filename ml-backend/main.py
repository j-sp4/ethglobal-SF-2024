from fastapi import FastAPI, File, UploadFile
from src.swap.start_swap import start_swap, get_swap_status, get_swap
from src.swap.models import SwapRequest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/start-swap")
async def start_swap(swap_request: SwapRequest):
    return start_swap(swap_request)

@app.get("/get_swap_status/{job_id}")
async def get_swap_status(job_id: str):
    return await get_swap_status(job_id)

@app.post("/get_swap")
async def get_swap(swap_request: SwapRequest):
    return await get_swap(swap_request)