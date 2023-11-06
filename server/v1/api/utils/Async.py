from ast import Call
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import threading
from typing import Callable, Generator

class Async:
    @classmethod
    def run_functions(
        cls,
        arr_func: list[Callable],
        arr_args: list[list],
        detach: bool = False
    ) -> list:
        """Run multiple functions with each arguments separately asynchronously

        Args:
            arr_func (list[Callable]): list of functions need to run
            arr_args (list[list]): arguments for each function

        Raises:
            Exception: the length of arr_func is not equal to the length of arr_args

        Returns:
            list: list of result for each function
        """
        if (len(arr_func) != len(arr_args)):
            raise Exception(f"Async.run_functions: the length of arr_func is {len(arr_func)} \
                            is not equal to the length of arr_args which is {len(arr_args)}")

        def wrapper(func: Callable, args: list):
            return func(*args)

        if not detach:
            return cls.run_single_func(wrapper, [[func, arr_args[i]] for i, func in enumerate(arr_func)])
            # with ThreadPoolExecutor() as executor:
            #     futures = [executor.submit(func, *arr_args[i]) for i, func in enumerate(arr_func)]
            #     return [future.result() for future in concurrent.futures.as_completed(futures)]

        else:
            threads: list[threading.Thread] = []
            for i, func in enumerate(arr_func):
                threads.append(threading.Thread(target=func, args=arr_args[i]))

            for thread in threads:
                thread.start()

            return []

    @classmethod
    def run_functions_stream(
        cls,
        arr_func: list[Callable],
        arr_args: list[list]
    ) -> Generator:
        if (len(arr_func) != len(arr_args)):
            raise Exception(f"Async.run_functions_stream: the length of arr_func is {len(arr_func)} \
                            is not equal to the length of arr_args which is {len(arr_args)}")
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(func, *arr_args[i]) for i, func in enumerate(arr_func)]
            for future in concurrent.futures.as_completed(futures):
                yield future.result()

    @classmethod
    def run_single_func(
        cls,
        func: Callable,
        arr_args: list[list]
    ) -> list:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(lambda args: func(*args), arr_args))

    @classmethod
    def run_single_func_stream(
        cls,
        func: Callable,
        arr_args: list[list]
    ) -> Generator:
        return cls.run_functions_stream([func] * len(arr_args), arr_args)
