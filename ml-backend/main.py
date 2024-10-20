import uvicorn
import os
from fastapi import FastAPI
from src.swap.api import start_swap, get_swap_status, get_swap
from src.swap.models import SwapModel
import roop.globals
from roop.core import run as roop_run
from settings import Settings

app = FastAPI()

# Initialize roop globals and run necessary setup
roop.globals.CFG = Settings('config.yaml')
roop_run()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/start-swap")
async def start_swap_api(swap_request: SwapModel):
    return await start_swap(swap_request)

@app.get("/get_swap_status/{job_id}")
async def get_swap_status_api(job_id: str):
    return await get_swap_status(job_id)

@app.post("/get_swap")
async def get_swap_api(swap_request: SwapModel):
    return await get_swap(swap_request)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("BACKEND_PORT"), reload=True)
