import os
import tempfile
import shutil
import pathlib
from ..helpers.logger import logger
from .models import SwapModel, SwapArgs
from starlette.concurrency import run_in_threadpool
from fastapi import HTTPException
from ..helpers.walrus import get_file_from_walrus, upload_file_to_walrus
from roop.core import batch_process_regular
import roop.globals
from .utils import map_mask_engine, process_entry
from .target_faces import calculate_and_get_target_faces
from .input_faces import process_src_images
from roop.ProcessMgr import ProcessMgr
from roop.ProcessOptions import ProcessOptions
from roop.utilities import conditional_download, resolve_relative_path

# Add this function definition
def get_processing_plugins(masking_engine):
    processors = {"faceswap": {}}
    if masking_engine is not None:
        if masking_engine == "Clip2Seg":
            logger.warning("Clip2Seg model is not available. Falling back to XSeg masking.")
            processors.update({"mask_xseg": {}})
        elif masking_engine == "XSeg":
            processors.update({"mask_xseg": {}})
        else:
            processors.update({masking_engine: {}})
    
    if roop.globals.selected_enhancer == 'GFPGAN':
        processors.update({"gfpgan": {}})
    elif roop.globals.selected_enhancer == 'Codeformer':
        processors.update({"codeformer": {}})
    elif roop.globals.selected_enhancer == 'DMDNet':
        processors.update({"dmdnet": {}})
    elif roop.globals.selected_enhancer == 'GPEN':
        processors.update({"gpen": {}})
    elif roop.globals.selected_enhancer == 'Restoreformer++':
        processors.update({"restoreformer++": {}})
    return processors

# Add this function to check and download required models
def ensure_models_exist():
    models_dir = resolve_relative_path('../models')
    logger.info(f"Models directory: {models_dir}")
    
    files_to_download = [
        'https://huggingface.co/countfloyd/deepfake/resolve/main/inswapper_128.onnx',
        'https://huggingface.co/countfloyd/deepfake/resolve/main/GFPGANv1.4.onnx',
        'https://huggingface.co/countfloyd/deepfake/resolve/main/xseg.onnx'
    ]
    
    for file_url in files_to_download:
        success = conditional_download(models_dir, [file_url])
        logger.info(f"Download of {file_url.split('/')[-1]} {'successful' if success else 'failed'}")
    
    # Check if files exist after download
    for file_url in files_to_download:
        file_name = file_url.split('/')[-1]
        file_path = os.path.join(models_dir, file_name)
        if os.path.exists(file_path):
            logger.info(f"File {file_name} exists at {file_path}")
        else:
            logger.error(f"File {file_name} does not exist at {file_path}")

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
        # Ensure models exist before processing
        ensure_models_exist()

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

        faces_middle, faces_quarter, faces_three_quarter = await calculate_and_get_target_faces(src_video_save_path)
        await process_src_images(target_image_save_path)
        
        # Initialize ProcessMgr here
        process_mgr = ProcessMgr()
        options = ProcessOptions(
            processordefines=get_processing_plugins(data.swap_args.selected_mask_engine),
            face_distance=data.swap_args.face_distance,
            blend_ratio=data.swap_args.blend_ratio,
            swap_mode=data.swap_args.swap_mode,
            selected_index=0,
            masking_text=data.swap_args.clip_text,
            imagemask=None,
            num_steps=data.swap_args.num_swap_steps,
            show_face_area=False
        )
        process_mgr.initialize(roop.globals.INPUT_FACESETS, roop.globals.TARGET_FACES, options)

        swap_stats = await swap_faces(src_video_save_path, target_image_save_path, data.swap_args, process_mgr)
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


async def swap_faces(src_video_path: str, target_image_path: str, swap_args: SwapArgs, process_mgr: ProcessMgr):
    global is_processing

    faces_middle, faces_quarter, faces_three_quarter = await calculate_and_get_target_faces(src_video_path)
    await process_src_images(target_image_path)
    list_files_process = [await process_entry(src_video_path)]

    # if roop.globals.CFG.clear_output:
    #     shutil.rmtree(roop.globals.output_path)

    # prepare_environment()

    roop.globals.selected_enhancer = swap_args.enhancer
    roop.globals.target_path = None
    roop.globals.distance_threshold = swap_args.face_distance
    roop.globals.blend_ratio = swap_args.blend_ratio
    roop.globals.keep_frames = swap_args.keep_frames
    roop.globals.wait_after_extraction = swap_args.wait_after_extraction
    roop.globals.skip_audio = swap_args.skip_audio
    roop.globals.face_swap_mode = swap_args.swap_mode
    roop.globals.no_face_action = swap_args.no_face_action
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




