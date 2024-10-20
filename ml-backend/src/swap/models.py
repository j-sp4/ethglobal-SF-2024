from pydantic import BaseModel
from typing import Literal

class SwapArgs(BaseModel):
    #default is None, this is the postprocesser
    enhancer: Literal["None", "Codeformer", "DMDNet", "GFPGAN", "GPEN", "Restoreformer++"]
    #default is selected
    swap_mode: Literal["selected", "first", "all_female", "all_male"]
    #relevant only when extracting frames
    keep_frames: bool
    #Wait for user key press before creating video 
    wait_after_extraction: bool
    #skips audio
    skip_audio: bool
    #Value 0.01 to 1.00 default is 0.65 Max Face Similarity Threshold
    face_distance: float
    # Value from 0 to 1 default is 0.65 only used with active post processing
    blend_ratio: float
    #mask engine
    selected_mask_engine: Literal["Clip2Seg", "DFL XSeg"]
    #"List of objects to mask and restore back on fake face, e.g sunglasses, hands, etc"
    clip_text: str
    #Default is In-Memory processing 
    processing_method: Literal["In-Memory processing", "File processing"]
    #"What to do if no face is detected"
    no_face_action: Literal["Use untouched original frame","Retry rotated", "Skip Frame", "Skip Frame if no similar face"]
    #"Use VR mode"
    vr_mode: bool
    #"Autorotate"
    autorotate: bool
    #Value from 1-5 default is 1 number of swapping steps
    num_swap_steps: int
    #confusing needs an editor
    imagemask: bool
   


class SwapModel(BaseModel):
    src_video_blob_name: str
    src_video_blob_id: str
    target_image_blob_name: str
    target_image_blob_id: str
    swap_args: SwapArgs

