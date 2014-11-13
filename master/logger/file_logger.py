from master.consts import PROJECT_HOME
import logging

logging.basicConfig(format='%(asctime)-15s [%(levelname)s - %(filename)s : %(funcName)s %(lineno)d] %(message)s ', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filename=PROJECT_HOME + '/logs/local.log', level=logging.INFO)


def logger():
    return logging




