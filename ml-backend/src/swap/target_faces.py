#TARGET_FACESETS refers to the target video

import util
import roop
import os

from roop.capturer import get_video_frame_total
from roop.face_util import extract_face_images
from roop.capturer import get_image_frame
from roop.FaceSet import FaceSet


def get_target_faces(files, frame_num):
    global IS_INPUT, SELECTION_FACES_DATA

    IS_INPUT = False
    thumbs = []
    #TODO: This is a temporary fix to get the first file in the list
    roop.globals.target_path = files[0].name
    if util.is_image(roop.globals.target_path) and not roop.globals.target_path.lower().endswith(('gif')):
        SELECTION_FACES_DATA = extract_face_images(roop.globals.target_path,  (False, 0))
        if len(SELECTION_FACES_DATA) > 0:
            for f in SELECTION_FACES_DATA:
                image = util.convert_to_gradio(f[1])
                thumbs.append(image)
        else:
            roop.globals.target_path = None
                
    elif util.is_video(roop.globals.target_path) or roop.globals.target_path.lower().endswith(('gif')):
        selected_frame = frame_num
        SELECTION_FACES_DATA = extract_face_images(roop.globals.target_path, (True, selected_frame))
        if len(SELECTION_FACES_DATA) > 0:
            for f in SELECTION_FACES_DATA:
                image = util.convert_to_gradio(f[1])
                thumbs.append(image)
        else:
            roop.globals.target_path = None

    if len(thumbs) == 1:
        roop.globals.TARGET_FACES.append(SELECTION_FACES_DATA[0][0])
    return thumbs

def calculate_and_get_target_faces(src_video_path: str):
    total_frames = get_video_frame_total(src_video_path)
    middle_frame = total_frames // 2
    quarter_frame = total_frames // 4
    three_quarter_frame = total_frames - quarter_frame

    get_target_faces(src_video_path, middle_frame)
    get_target_faces(src_video_path, quarter_frame)
    get_target_faces(src_video_path, three_quarter_frame)