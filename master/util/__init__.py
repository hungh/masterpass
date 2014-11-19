import json


def create_json_status(bool_stat, message):
    """
    Generate json format for status and message
    :param bool_stat: True/False
    :param message: string
    :return: json string format
    """
    return json.dumps({'stat': bool_stat, 'msg': message})