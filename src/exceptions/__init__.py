import sys

def error_message_detail(error, error_detail: sys):
    try:
        exc_info = error_detail.exc_info()
    except Exception:
        return f"Error occured: {error} (error_detail has no exc_info)"
    if exc_info is None or exc_info[2] is None:
        return f"Error occured: {error} (no traceback available)"
    _, _, exc_tb = exc_info
    if exc_tb is None:
        return f"Error occured: {error} (traceback is None)"
    file_name = exc_tb.tb_frame.f_code.co_filename
    return f"Error occured in python script name [{file_name}] line number [{exc_tb.tb_lineno}] error message[{error}]"

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
    def __str__(self):
        return self.error_message