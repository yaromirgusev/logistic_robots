import requests
import time
from utils.up_down import up_tray, down_tray
from utils.robot_move import send_move_command
from utils.robot_status import wait_until_robot_completes_move
from scan_qr import read_qr_stream
import logging
from scan_qr import read_qr_stream

logging.basicConfig(
    level=logging.INFO,  
    format='%(asctime)s - %(levelname)s - %(message)s',  
    handlers=[
        logging.FileHandler("app.log"),  
        logging.StreamHandler()  
    ]
)

def point_to_point():
    point = input("Введите название точки : ")
    robot = input("Введите название робота : ")
    down_tray(robot)
    time.sleep(10)
    move_result = send_move_command(robot, point)  # Отправляем команду на движение
    logging.info(f"Move command status: {move_result}")
    time.sleep(0.5)
    wait_until_robot_completes_move(robot)
    time.sleep(0.5)
    up_tray(robot)

def full_pipeline(robot, starting_point : str, stay_point : str, end_point : str):
    down_tray(robot)

    move_result = send_move_command(robot, stay_point)
    logging.info(f"Move command status: {move_result}")
    wait_until_robot_completes_move(robot)

    up_tray(robot)

    qr_stream = None
    while not qr_stream:
        qr_stream = read_qr_stream()

    down_tray(robot)

    move_result = send_move_command(robot, end_point)
    logging.info(f"Move command status: {move_result}")
    wait_until_robot_completes_move(robot)

    move_result = send_move_command(robot, starting_point)
    logging.info(f"Move command status: {move_result}")
    wait_until_robot_completes_move(robot)

for i in range(5):
    full_pipeline('Robot12', 'Mendeleev', 'Apollo', 'Verhov')





