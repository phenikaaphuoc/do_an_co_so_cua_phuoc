import cv2
from resources.utility import xywh2xyxy
import math
import numpy as np
from mtcnn import MTCNN
class Detection:
    def __init__(self):
        caffemodel = r"resources/detection_model/Widerface-RetinaFace.caffemodel"
        deploy = r"resources/detection_model/deploy.prototxt"
        self.detector = cv2.dnn.readNetFromCaffe(deploy, caffemodel)
        self.detector_confidence = 0.6

    def get_bbox(self, img):
        height, width = img.shape[0], img.shape[1]
        aspect_ratio = width / height
        if img.shape[1] * img.shape[0] >= 192 * 192:
            img = cv2.resize(img,
                             (int(192 * math.sqrt(aspect_ratio)),
                              int(192 / math.sqrt(aspect_ratio))), interpolation=cv2.INTER_LINEAR)

        blob = cv2.dnn.blobFromImage(img, 1, mean=(104, 117, 123))
        self.detector.setInput(blob, 'data')
        out = self.detector.forward('detection_out').squeeze()
        max_conf_index = np.argmax(out[:, 2])
        left, top, right, bottom = out[max_conf_index, 3]*width, out[max_conf_index, 4]*height, \
                                   out[max_conf_index, 5]*width, out[max_conf_index, 6]*height
        bbox = [int(left), int(top), int(right-left+1), int(bottom-top+1)]
        #x1,y1,w,h
        return bbox
    
det = Detection()
detector = MTCNN()

def mtcnn_face_detect(frame,image_input = "bgr"):
    if image_input == "bgr":
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(frame)
    face = []
    if faces:
        confidence_scores = [face['confidence'] for face in faces]
        max_confidence_index = confidence_scores.index(max(confidence_scores))
        #x,y,w,h
        face = faces[max_confidence_index]['box']
    return xywh2xyxy([face])
    
def face_detect(frame):
    '''
    return [[x1,y1,x2,y2],[...],...]
    '''
    return xywh2xyxy([det.get_bbox(frame)])
