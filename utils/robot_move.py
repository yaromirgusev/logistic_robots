import requests
import time

def send_move_command(robot : str, point : str, angle : int = None):
    if angle:
        json_to_send = {
            'Type': 'Move',
            'BindRobotName': robot,
            'Param': {
                'Nodes': [{'NodeName': point}],
                'TargetAngle': angle  # поворот на angle градусов
            }
        }

    else:
        json_to_send = {
            'Type': 'Move',
            'BindRobotName': robot,
            'Param': {
                'Nodes': [{'NodeName': point}]
            }
        }   

    response = requests.post('http://192.168.124.5:8090/wcs/task', json=json_to_send)
    time.sleep(0.5)
    return response.json()