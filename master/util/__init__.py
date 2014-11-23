from master.encryption.encrypt_bfish import MyBlowFish
from master.sesscontroller.session_controller import SessionController
from master.consts import SESSION_USER_ID
import json


def create_json_status(bool_stat, message):
    """
    Generate json format for status and message
    :param bool_stat: True/False
    :param message: string
    :return: json string format
    """
    return json.dumps({'stat': bool_stat, 'msg': message})


def gen_enc_string(secret_key, password):
    """
    Get encrypted string of a pws entry of an owner
    :param secret_key: string key
    :param password: string (clear text)
    :return: string encrypted string
    """
    return MyBlowFish(secret_key).encrypt(password)


def get_clear_text(secret_key, enc):
    """
    Get clear text of an pws entry
    :param env: string environment name
    :param user: string user of a pws entry
    :param pws_entry: master.beans.pws_entries.PwsEntry
    :param owner: string current log-in user id
    :return: clear text of password entry (in a pws)
    """
    password_entry = MyBlowFish(secret_key).decrypt(enc)
    try:
        return password_entry.decode('utf-8')
    except UnicodeDecodeError:
        return None


def get_current_login_user_id(request_handler):
    """
    Return the current login id in HTTP session
    :param request_handler: master.handler.CustomHTTPHandler (http.server.SimpleHTTPRequestHandler)
    """
    session_bean, was_created_new = SessionController().get_session(request_handler, will_create_new=False)
    return session_bean.get_attribute(SESSION_USER_ID)