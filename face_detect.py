import numpy as np
import cv2

def get_facepos(img_path):
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_eye_tree_eyeglasses.xml')

    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    result = []
    for (x,y,w,h) in faces:
        face_dst = {
            "x": np.asscalar(x),
            "y": np.asscalar(y),
            "w": np.asscalar(w),
            "h": np.asscalar(h)
        }
        eyes_dst = []
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            eye_pos = {
                "x": np.asscalar(ex),
                "y": np.asscalar(ey),
                "w": np.asscalar(ew),
                "h": np.asscalar(eh)
            }
            eyes_dst.append(eye_pos)
        result.append({
            "face": face_dst,
            "eyes": eyes_dst
        })
    return result
