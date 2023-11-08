import traceback
from typing import Any
from colorama import Fore

class FlaskLog:
    @staticmethod
    def info(msg: Any) -> None:
        print(Fore.GREEN + "INFO: " + str(msg), flush=True)

    @staticmethod
    def warn(msg: Any) -> None:
        print(Fore.YELLOW + "WARNING: " + str(msg), flush=True)

    @staticmethod
    def err(msg: Any) -> None:
        print(Fore.RED + "ERROR: " + str(msg), flush=True)

    @staticmethod
    def print_except(e: Exception) -> None:
        traceback.print_exc()
