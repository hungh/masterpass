from master.filters.app_filter import ApplicationFilter
from master.filters.session_filter import SessionFilter


def filter_chain(request_handler):
    """
    a filter chain mappings
    """
    l1, m1 = ApplicationFilter().filter(request_handler)
    l2, m2 = SessionFilter().filter(request_handler)
    if l1 and l2 is False:
        return False, m1 + m2
    return True, ""


