import cv2
import tensorflow.keras
import numpy as np
import ctypes
from PIL import Image, ImageOps

# Google Teachable Machine 으로 학습한 keras_model.h5의 경로
MODEL_FILE_NAME = 'Input your keras_model.h5 Path'

# 이미지 전처리
def preprocessing(frame):
    size = (224, 224)
    frame_resized = cv2.resize(frame, size, interpolation=cv2.INTER_AREA)
    frame_normalized = (frame_resized.astype(np.float32) / 127.0) - 1
    frame_reshaped = frame_normalized.reshape((1, 224, 224, 3))
    
    return frame_reshaped

# 간단한 다이얼로그 창 표시
def callDialog():
    msg = ctypes.windll.user32.MessageBoxW(None, "거북목 조심!", "경고창", 0)

if __name__ == "__main__":
    model = tensorflow.keras.models.load_model(MODEL_FILE_NAME)

    # 디바이스 내 카메라 사용
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 420)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 420)

    while True:
        ret, frame = capture.read()
        if not ret:
            print("Image Load Failed")

        # 이미지 좌우 반전
        frame_fliped = cv2.flip(frame, 1)
        
        cv2.imshow("Detecting Tuttle Neck", frame_fliped)

        # 'q' 버튼을 누르면 종료
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

        # 데이터 전처리
        preprocessed = preprocessing(frame_fliped)
        
        # 전처리된 데이터를 통한 예측
        prediction = model.predict(preprocessed)

        # prediction[0, 0] : no tuttle neck, prediction[0, 1] : tuttle neck
        if prediction[0, 0] < prediction[0, 1]:
            print("거북목 주의!")
            print(prediction)
            callDialog()
            
        else:
            print("정상 상태")

    capture.release()
    cv2.destroyAllWindows()
