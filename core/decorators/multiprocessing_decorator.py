from multiprocessing import Process
import logging

logger = logging.getLogger(__name__)


def multi_process_run(func):
    def wrapper(*args, **kwargs):
        """

        Args:
            fn: function to be run into multiprocess way
            args: tuple of args --> (arg1. arg2, ...)

        Returns:

        """
        proc = Process(target=func, args=args, kwargs=kwargs)
        proc.start()
        proc.join()

        exit_code = proc.exitcode

        return
    return wrapper
