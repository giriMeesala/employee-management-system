import insightface
import numpy as np

app = insightface.app.FaceAnalysis()

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)

def get_face_embedding(frame):

    faces = app.get(frame)

    if len(faces) == 0:
        return None

    embedding = faces[0].embedding

    return embedding