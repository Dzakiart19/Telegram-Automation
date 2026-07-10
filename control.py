import threading

restart_event = threading.Event()
auth_key_dead_event = threading.Event()


def request_restart():
    restart_event.set()


def is_restart_requested():
    return restart_event.is_set()


def clear_restart():
    restart_event.clear()


def mark_auth_key_dead():
    """Tandai bahwa session saat ini sudah dicabut Telegram (AuthKeyDuplicatedError).
    Restart cepat dengan session yang sama tidak akan membantu — dipakai main.py
    untuk melakukan backoff panjang alih-alih crash-loop 5 detik."""
    auth_key_dead_event.set()


def is_auth_key_dead():
    return auth_key_dead_event.is_set()


def clear_auth_key_dead():
    auth_key_dead_event.clear()
