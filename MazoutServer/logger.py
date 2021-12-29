"""This is the logging system."""

from sys import stderr
from . import __version__
from time import time


class Logger:
    def __init__(self) -> None:
        self.log_file = "mazout.log"
        self.__write(f"\n>>> This is Mazout, version {__version__}. Run at {time()} seconds since Unix epoch.")

    def log_err(self, error: str) -> None:
        self.__write(f"[{time()}] ERROR : " + error)
        self.__print_to_stderr(error)

    def log(self, to_log: str):
        self.__write(f"[{time()}] LOG : " + to_log)
        print(to_log)

    def __write(self, to_write: str) -> None:
        with open(self.log_file, 'a') as f:
            f.write("\n" + to_write)

    def __print_to_stderr(self, to_print: str) -> None:
        print(to_print, file=stderr)
