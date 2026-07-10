import threading

restart_event = threading.Event()


def request_restart():
    restart_event.set()


def is_restart_requested():
    return restart_event.is_set()


def clear_restart():
    restart_event.clear()
