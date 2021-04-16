import cv2
import tensorflow.keras
import numpy as np
import beepy
import ctypes
from PIL import Image, ImageOps

MODEL_FILE_NAME = './.opencv-project2/datas/keras_model.h5'

def preprocessing(frame):
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))

    return frame_reshaped


def callDialog():
    msg = ctypes.windll.user32.MessageBoxW(None, "거북목 조심!", "경고창", 0)


if __name__ == "__main__":
    model = tensorflow.keras.models.load_model(MODEL_FILE_NAME)

    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Image Load Failed")

        frame_fliped = cv2.flip(frame, 1)

        cv2.imshow("거북목 탐지 프로그램", frame_fliped)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        preprocessed = preprocessing(frame_fliped)
        prediction = model.predict(preprocessed)

        if prediction[0, 0] < prediction[0, 1]:
            print("거북목 주의!")
            callDialog()
            print(prediction)
            
        else:
            print("정상 상태")

    capture.release()
    cv2.destroyAllWindows()