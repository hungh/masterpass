from master.consts import BLACK_LIST, SPEED_THRESHOLD
from master.logger.file_logger import logger
from time import time
import threading

threadLock = threading.Lock()
ip_dict = dict()


class IPBlocker:

    @staticmethod
    def should_block(client_address):
        """
        Determine if 'client_address' should be blocked or not
        :param client_address: string ip_adress of client
        :return: boolean true if the client's ip address should be blocked, false otherwise
        """
        logger().info("Examining ip_address:" + client_address)

        if IPBlocker.is_in_black_list(client_address):
            logger().warn('client ip:' + client_address + ' is in the blacklist')
            return True

        new_timestamp = 0
        try:
            new_timestamp = time()
            old_timestamp = ip_dict[client_address]
            time_gap = new_timestamp - old_timestamp
            logger().info('time-gap for \'' + client_address + '\':' + str(time_gap))
            if time_gap <= SPEED_THRESHOLD:
                logger().warn(client_address + ' is being blocked')
                return True
        except KeyError:
            pass
        finally:
            IPBlocker.update_ip_pool(client_address, new_timestamp)

        return False

    @staticmethod
    def update_ip_pool(client_address, new_timestamp):
        threadLock.acquire()
        ip_dict[client_address] = new_timestamp
        logger().info('Updating dict for ' + client_address)
        threadLock.release()

    @staticmethod
    def is_in_black_list(client_address):
        return client_address.strip() in BLACK_LIST
