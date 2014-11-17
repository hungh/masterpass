from master.consts import USER_HOME
import logging

logging.basicConfig(format='%(asctime)-15s [%(levelname)s - %(filename)s : %(funcName)s %(lineno)d] %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=USER_HOME + '/logs/local.log', level=logging.INFO)


def logger():
    return logging




