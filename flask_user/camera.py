import cv2
import os, io
from google.cloud import vision
from google.cloud.vision import types
import time
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'SA.json'

faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

faceArray = []
def detect_faces(path):
    """Detects faces in an image."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations

    # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

    for face in faces:

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        #[face bounds, anger, joy, surprise, sorrow] 
        faceArray = [(vertices), likelihood_name[face.anger_likelihood], likelihood_name[face.joy_likelihood],  likelihood_name[face.surprise_likelihood], likelihood_name[face.sorrow_likelihood]]
        return faceArray

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))


class VideoCamera(object):
    def __init__(self):
       self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()

    def change_frame(self):
        global faceArray
        ret, frame = self.video.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(35, 35))

        for (x, y, w, h) in face:
            cv2.rectangle(frame, (x, y), (w+x, h+y), (200, 50, 30), 2)
            cropped_face = frame[y:h+y, x:w+x]
            cv2.imwrite('./faces/currentface.jpg', cropped_face)
        
        detect_faces("./faces/currentface.jpg")

  
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

        




