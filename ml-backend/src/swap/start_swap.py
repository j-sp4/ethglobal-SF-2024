import os
import tempfile
from helpers.logger import logger
from swap.models import SwapModel
from starlette.concurrency import run_in_threadpool
from fastapi import HTTPException
from helpers.walrus import get_file_from_walrus, upload_file_to_walrus
from roop.core import batch_process_regular
import os
import shutil
import pathlib
import roop.utilities as util
import roop.globals
from roop.face_util import extract_face_images, create_blank_image
from roop.capturer import get_video_frame, get_video_frame_total, get_image_frame
from roop.ProcessEntry import ProcessEntry
from roop.ProcessOptions import ProcessOptions
from roop.FaceSet import FaceSet
from swap.utils import index_of_no_face_action, map_mask_engine, process_entry
from swap.target_faces import calculate_and_get_target_faces
from swap.input_faces import process_src_images
from swap.models import SwapModel, SwapArgs

DIRECTORY = tempfile.gettempdir()
UPLOAD_DIRECTORY = os.path.join(DIRECTORY, "uploads")

src_video_bucket_name = os.getenv("GOOGLE_SRC_VIDEO_BUCKET_NAME")
target_image_bucket_name = os.getenv("GOOGLE_TARGET_IMAGE_BUCKET_NAME")
swap_video_bucket_name = os.getenv("GOOGLE_SWAP_VIDEO_BUCKET_NAME")

input_faces = None
target_faces = None

async def get_swap_implementation(data: SwapModel):
    logger.debug(data)
    print("Data coming to get_swap_implementation", data)
    src_video_blob_name = data.src_video_blob_name
    src_video_blob_id = data.src_video_blob_id
    target_image_blob_name = data.target_image_blob_name
    target_image_blob_id = data.target_image_blob_id
    swap_args = data.swap_args
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    src_video_save_path = os.path.join(UPLOAD_DIRECTORY, src_video_blob_name)
    target_image_save_path = os.path.join(UPLOAD_DIRECTORY, target_image_blob_name)
    logger.debug(src_video_save_path)
    logger.debug(target_image_save_path)
    try:
        # await run_in_threadpool(
        #     get_file_from_gcs, src_video_blob_name, src_video_save_path, swap_video_bucket_name
        # )
        # await run_in_threadpool(
        #     get_file_from_gcs, target_image_blob_name, target_image_save_path, target_image_bucket_name
        # )
        await run_in_threadpool(
            get_file_from_walrus, src_video_blob_id, src_video_save_path
        )
        await run_in_threadpool(
            get_file_from_walrus, target_image_blob_id, target_image_save_path
        )
        logger.debug("file was retrieved from GCS and saved locally")

        swap_stats = await swap_faces(src_video_save_path, target_image_save_path, swap_args)
        logger.debug(swap_stats)
        logger.debug("swap complete")
        if swap_stats:
            swap_video_blob_id = await run_in_threadpool(
                upload_file_to_walrus,
                src_video_save_path,
            )
            return {
                "swap_video_blob_id": swap_video_blob_id,
                "stats": swap_stats,
            }
        else:
            logger.error("Failed to analyze the file")
            raise HTTPException(status_code=500, detail="Failed to swap faces")

    except Exception as e:
        # If you want to be specific with the errors, you can handle different exceptions separately.
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


def swap_faces(src_video_path: str, target_image_path: str, swap_args: SwapArgs):
    global is_processing
    calculate_and_get_target_faces(src_video_path)
    process_src_images(target_image_path)
    list_files_process = [process_entry(src_video_path)]

    if roop.globals.CFG.clear_output:
        shutil.rmtree(roop.globals.output_path)

    # prepare_environment()

    roop.globals.selected_enhancer = swap_args.enhancer
    roop.globals.target_path = None
    roop.globals.distance_threshold = swap_args.face_distance
    roop.globals.blend_ratio = swap_args.blend_ratio
    roop.globals.keep_frames = swap_args.keep_frames
    roop.globals.wait_after_extraction = swap_args.wait_after_extraction
    roop.globals.skip_audio = swap_args.skip_audio
    roop.globals.face_swap_mode = swap_args.swap_mode
    roop.globals.no_face_action = index_of_no_face_action(swap_args.no_face_action)
    roop.globals.vr_mode = swap_args.vr_mode
    roop.globals.autorotate_faces = swap_args.autorotate
    mask_engine = map_mask_engine(swap_args.selected_mask_engine, swap_args.clip_text)

    if roop.globals.face_swap_mode == 'selected':
        if len(roop.globals.TARGET_FACES) < 1:
            raise ValueError('No Target Face selected!')

    is_processing = True            
    roop.globals.execution_threads = roop.globals.CFG.max_threads
    roop.globals.video_encoder = roop.globals.CFG.output_video_codec
    roop.globals.video_quality = roop.globals.CFG.video_quality
    roop.globals.max_memory = roop.globals.CFG.memory_limit if roop.globals.CFG.memory_limit > 0 else None

    processing_method = swap_args.processing_method

    batch_process_regular(list_files_process, mask_engine, swap_args.clip_text, processing_method == "In-Memory processing", swap_args.imagemask, swap_args.num_swap_steps, progress, SELECTED_INPUT_FACE_INDEX)
    is_processing = False
    outdir = pathlib.Path(roop.globals.output_path)
    outfiles = [str(item) for item in outdir.rglob("*") if item.is_file()]
    return outfiles

