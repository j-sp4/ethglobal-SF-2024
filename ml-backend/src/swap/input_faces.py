#INPUT_FACESETS refers to the source Images
import roop.globals
import os
from roop.face_util import extract_face_images
from roop.capturer import get_image_frame
from roop.FaceSet import FaceSet
from roop.utilities import mkdir_with_umask, unzip, has_image_extension


async def process_src_images(srcfiles):
    global SELECTION_FACES_DATA, IS_INPUT, input_faces, face_selection, last_image
    
    IS_INPUT = True

    if srcfiles is None or len(srcfiles) < 1:
        return
    
    thumbs = []
    for f in srcfiles:    
        source_path = f
        if source_path.lower().endswith('fsz'):
            unzipfolder = os.path.join(os.environ["TEMP"], 'faceset')
            if os.path.isdir(unzipfolder):
                files = os.listdir(unzipfolder)
                for file in files:
                    os.remove(os.path.join(unzipfolder, file))
            else:
                os.makedirs(unzipfolder)
            mkdir_with_umask(unzipfolder)
            unzip(source_path, unzipfolder)
            is_first = True
            face_set = FaceSet()
            for file in os.listdir(unzipfolder):
                if file.endswith(".png"):
                    filename = os.path.join(unzipfolder,file)
                    SELECTION_FACES_DATA = await extract_face_images(filename,  (False, 0))
                    for f in SELECTION_FACES_DATA:
                        face = f[0]
                        face.mask_offsets = (0,0,0,0,1,20)
                        face_set.faces.append(face)
                        if is_first: 
                            is_first = False
                        face_set.ref_images.append(get_image_frame(filename))
            if len(face_set.faces) > 0:
                if len(face_set.faces) > 1:
                    face_set.AverageEmbeddings()
                roop.globals.INPUT_FACESETS.append(face_set)
                                        
        elif has_image_extension(source_path):
            roop.globals.source_path = source_path
            SELECTION_FACES_DATA = extract_face_images(roop.globals.source_path,  (False, 0))
            for f in SELECTION_FACES_DATA:
                face_set = FaceSet()
                face = f[0]
                face.mask_offsets = (0,0,0,0,1,20)
                face_set.faces.append(face)
                roop.globals.INPUT_FACESETS.append(face_set)
                

