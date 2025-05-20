import cv2
import time
from pyzbar import pyzbar
from datetime import datetime

def decode_qr(frame):
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        decoded = pyzbar.decode(gray)
        for obj in decoded:
            return obj.data.decode('utf-8')
        return None
    except Exception as e:
        print(f"Ошибка декодирования: {e}")
        return None

def read_qr_stream():
    RTSP_URL = 'rtsp://admin:admin@192.168.124.101:554/main'
    CHECK_INTERVAL = 0.01  # 100 ms
    
    while True:
        # print(1)
        cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)
        if not cap.isOpened():
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Ошибка подключения")
            time.sleep(1)
            continue

        try:
            ret, frame = cap.read()
            if not ret:
                raise Exception("Не удалось получить кадр")
            
            qr_data = decode_qr(frame)
            if qr_data:
                return qr_data

                
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Ошибка: {str(e)}")
        
        finally:
            cap.release()
        
        time.sleep(CHECK_INTERVAL)