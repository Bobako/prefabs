import logging
import sys
import traceback

from cfg import LOGS_PATH

logging.basicConfig(format='%(asctime)s  ---  %(message)s \n\n', level=logging.WARNING, filename=LOGS_PATH)

while True:
    try:                                            # какая то вохможно ошибочная хуйня (можно туда мейн на проде запихнуть кста)
        a = 9/0
    except Exception:
        msg, type_, tb = sys.exc_info()
        tb = '\n'.join(traceback.format_tb(tb))
        logging.warning(f"{msg}, {type_}\n {tb}")   # пишем приятные логи с полным трейсом по ошибке, кайф