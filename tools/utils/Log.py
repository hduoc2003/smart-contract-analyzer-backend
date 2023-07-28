import traceback
from typing import Any

from colorama import Fore


class Log:
    @staticmethod
    def info(msg: Any) -> None:
        print(Fore.GREEN + str(msg))

    @staticmethod
    def warn(msg: Any) -> None:
        print(Fore.YELLOW + str(msg))

    @staticmethod
    def err(msg: Any) -> None:
        print(Fore.RED + str(msg))

    @staticmethod
    def print_except(e: Exception) -> None:
        traceback.print_exc()
