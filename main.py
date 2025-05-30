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

for i in range(3):
    full_pipeline('Robot11', 'Mendeleev', 'Apollo', 'Verhov')


# Нужна система пар чтобы при задаче имя робота, 
# Имя точки, Тип действия на точке ,(подъем, опускание, подъем+опускание, ожидание, смена этажа)
# Нужно разбить функции на отдельные команды
# пусть функция подъема будет вызываться написанием u, просто перемещение m (и угол поворота в этой точке при необходимости),
# опускание d, ожидание w, смена этажа c(change)n(где n цифра на который меняется этаж) 
# то есть нужна под функция диспетчер которая вызывает ту или ину функцию в зависимости от буквы

# Пример full_pipeline('Robot11 Apollo u','Robot11 Mendeleev w ','Robot12 Apollo m') - каждой команде
# приписывается имя робота и так можно задать любое кол-во роботов для одной зоны 
# Пример 2 full_pipeline(Robot11, 'Apollo u','Mendeleev w','Apollo m') - мы задаем 
# имя робота и стоит его маршрут пермещения, но так нельзя добавить другого робота
# Функции подъема, например, можно реализовать не зависимо от точки, тогда целесообразнее
# сначала писать сначало команду, а потом уже точку (т.е. "'m Apollo', 'u', и т. д.")

# нужен способ маштабирование для N роботов, либо через распараленирование
# Либо последовательная задача комант в зависимости от количества роботов
# возможно стоит реализовать сначала не унивфецированный код, а просто для 
# N машин

# Добавить простой счетчик который можно вкл/выкл на случай если 
# понадобится перевозить открытый биоматериал (то есть надо будет типа ездить в зону стререлизации)