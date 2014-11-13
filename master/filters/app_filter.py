from master.filters.abstract_filter import AbstractFilter
from master.logger.file_logger import logger


class ApplicationFilter(AbstractFilter):

    """
    All requests have to go through this filter
    """
    def __init__(self):
        pass

    def filter(self, request_handler):
        logger().debug(' application filter')
        return True, ""


