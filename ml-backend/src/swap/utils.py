import util
import roop
import os

from models import ProcessEntry
from roop.capturer import get_video_frame_total
from roop.face_util import extract_face_images
from roop.capturer import get_image_frame
from roop.FaceSet import FaceSet


def map_mask_engine(selected_mask_engine, clip_text):
    if selected_mask_engine == "Clip2Seg":
        mask_engine = "mask_clip2seg"
        if clip_text is None or len(clip_text) < 1:
          mask_engine = None
    elif selected_mask_engine == "DFL XSeg":
        mask_engine = "mask_xseg"
    else:
        mask_engine = None
    return mask_engine


def index_of_no_face_action(dropdown_text):
    global no_face_choices

    return no_face_choices.index(dropdown_text) 

def process_entry(video_path: str):
    return ProcessEntry(filename=video_path, startframe=0, endframe=get_video_frame_total(video_path), fps=50)

##This refers to the source video
def on_selected_face():
    global IS_INPUT, SELECTED_FACE_INDEX, SELECTION_FACES_DATA
    
    fd = SELECTION_FACES_DATA[SELECTED_FACE_INDEX]
    image = util.convert_to_gradio(fd[1])
    if IS_INPUT:
        handle_input_face(fd)
    else:
        handle_target_face(fd)

def handle_input_face(fd):
    face_set = FaceSet()
    fd[0].mask_offsets = (0,0,0,0,1,20)
    face_set.faces.append(fd[0])
    roop.globals.INPUT_FACESETS.append(face_set)

def handle_target_face(fd):
    roop.globals.TARGET_FACES.append(fd[0])
