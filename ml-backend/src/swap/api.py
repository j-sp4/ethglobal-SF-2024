from .start_swap import get_swap_implementation
from .models import SwapModel
from fastapi import HTTPException
from ..helpers.logger import logger
from fastapi.responses import JSONResponse
import traceback
import asyncio
import uuid

running_tasks: dict[str, dict] = {}

async def start_swap(data: SwapModel):
    async def run_swap():
        try:
            result = await get_swap_implementation(data)
        except:
            logger.error("Exception occured during file swap!")
            running_tasks[job_id] = {
                **running_tasks[job_id],
                "status": "FAILED",
                "error": traceback.format_exc(),
            }
            raise
        running_tasks[job_id] = {
            **running_tasks[job_id],
            "status": "SUCCEEDED",
            "progress": 100,
            "result": result,
        }

    job_id = str(uuid.uuid4())
    logger.debug("Starting swap in the background...")
    initial_task_status = running_tasks[job_id] = {
        "id": job_id,
        "status": "IN_PROGRESS",
        "progress": 0,
    }
    asyncio.create_task(run_swap())  # run coroutine in backgroud
    return JSONResponse(
        content=initial_task_status,
        status_code=202,
    )
async def get_swap_status(job_id: str):
    if job_id not in running_tasks:
        raise HTTPException(status_code=404, detail="Job not found")
    return running_tasks[job_id]

async def get_swap(data: SwapModel):
    return JSONResponse(
        await get_swap_implementation(data), status_code=201
    )  # HTTP 201 Created
