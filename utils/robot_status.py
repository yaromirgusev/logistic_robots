import requests
import time
import logging

def get_send_process_id(robot_name, robots_data):
    for robot in robots_data["Data"]["RobotsState"]:
        if robot["RobotInfo"]["Name"] == robot_name:
            return robot["Wcs"]["TaskId"]
    return None

def check_robot_status(robot):
    response = requests.get('http://192.168.124.5:8090/wcs/robots/state')
    robots_data = response.json()

    result = get_send_process_id(robot, robots_data)
    # logging.info(f"TaskId для {robot}: {result}")
    return result

def wait_until_robot_completes_move(robot_name):
    while True:
        status = check_robot_status(robot_name)
        if status == "":  # Условия
            break
        time.sleep(0.5)  # Небольшая задержка между проверками