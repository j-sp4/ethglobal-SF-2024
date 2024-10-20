#TARGET_FACESETS refers to the target video

import roop.globals
from roop.utilities import is_image, is_video, convert_to_rgb
from roop.capturer import get_video_frame_total
from roop.face_util import extract_face_images
from ..helpers.logger import logger
from roop.ProcessMgr import ProcessMgr
from roop.ProcessOptions import ProcessOptions


async def get_target_faces(files, frame_num, process_mgr):
    global IS_INPUT, SELECTION_FACES_DATA

    IS_INPUT = False
    thumbs = []
    logger.debug(f"Received files: {files}, frame_num: {frame_num}")

  
    roop.globals.target_path = files[0]
    logger.debug(f"Set target path: {files[0]}")

    if is_image(roop.globals.target_path) and not roop.globals.target_path.lower().endswith(('gif')):
        SELECTION_FACES_DATA = await process_mgr.extract_face_images(roop.globals.target_path, (False, 0))
        logger.debug(f"Extracted face images from image: {SELECTION_FACES_DATA}")
        if len(SELECTION_FACES_DATA) > 0:
            for f in SELECTION_FACES_DATA:
                image = convert_to_rgb(f[1])
                thumbs.append(image)
        else:
            logger.warning("No faces found in image.")
            roop.globals.target_path = None
                
    elif is_video(roop.globals.target_path) or roop.globals.target_path.lower().endswith(('gif')):
        SELECTION_FACES_DATA = await process_mgr.extract_face_images(roop.globals.target_path, (True, frame_num))
        logger.debug(f"Extracted face images from video/gif: {SELECTION_FACES_DATA}")
        if len(SELECTION_FACES_DATA) > 0:
            for f in SELECTION_FACES_DATA:
                image = convert_to_rgb(f[1])
                thumbs.append(image)
        else:
            logger.warning("No faces found in video/gif.")
            roop.globals.target_path = None

    if len(thumbs) == 1:
        logger.info(f"SELECTION_FACES_DATA: {SELECTION_FACES_DATA}")
        roop.globals.TARGET_FACES.append(SELECTION_FACES_DATA[0][0])
    else:
        logger.warning("No unique target face found.")
        
    logger.debug(f"Returning thumbs: {thumbs}")
    return thumbs

async def calculate_and_get_target_faces(src_video_path: str):
    total_frames = get_video_frame_total(src_video_path)
    middle_frame = total_frames // 2
    quarter_frame = total_frames // 4
    three_quarter_frame = total_frames - quarter_frame

    # Initialize ProcessMgr here with minimal options
    process_mgr = ProcessMgr()
    minimal_options = ProcessOptions(
        processordefines={},  # Empty dictionary for processor definitions
        face_distance=0.6,
        blend_ratio=1.0,
        swap_mode="selected",
        selected_index=0,
        masking_text="",
        imagemask=None,
        num_steps=1,  # Default value for num_steps
        show_face_area=False  # Default value for show_face_area
    )
    process_mgr.initialize([], [], minimal_options)

    faces_middle = await get_target_faces([src_video_path], middle_frame, process_mgr)
    faces_quarter = await get_target_faces([src_video_path], quarter_frame, process_mgr)
    faces_three_quarter = await get_target_faces([src_video_path], three_quarter_frame, process_mgr)

    return faces_middle, faces_quarter, faces_three_quarter
