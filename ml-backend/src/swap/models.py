from pydantic import BaseModel
from typing import Literal

class SwapArgs(BaseModel):
    enhancer: str
    swap_mode: Literal["selected", "first", "all_female", "all_male"]
    keep_frames: int
    wait_after_extraction: int
    skip_audio: bool
    face_distance: float
    blend_ratio: float
    selected_mask_engine: Literal["Clip2Seg", "DFL XSeg"]
    clip_text: str
    processing_method: str
    no_face_action: str
    vr_mode: bool
    autorotate: bool
    num_swap_steps: int
    imagemask: bool
   


class SwapModel(BaseModel):
    src_video_blob_name: str
    src_video_blob_id: str
    target_image_blob_name: str
    target_image_blob_id: str
    swap_args: SwapArgs
