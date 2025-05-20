import requests
import logging
import time

def up_tray(number):
    json_to_send = {
            'Action':'Up'
        }
    core(json_to_send, number)
    time.sleep(9)

def down_tray(number):
    json_to_send = {
            'Action':'Down'
        }
    core(json_to_send, number)
    time.sleep(9)

def core(json_to_send, number):
    robot_number = number.replace("Robot", "") 
    ip_address = f"192.168.76.{robot_number}"
    url = f"http://{ip_address}:8080/agv/actor/lmr"
    response = requests.post(url, json=json_to_send)
    logging.info(f"Command status: {response.json()}")