# -*- coding: UTF-8 -*-
import logging
import sys
from typing import List, Dict, Union, Tuple

PRINT_LEVELV_NUM = 60
logging.addLevelName(PRINT_LEVELV_NUM, "PRINT")


def printlog(
        self: logging.Logger,
        msg: str,
        *args,
        **kwargs
):
    if self.isEnabledFor(PRINT_LEVELV_NUM):
        self._log(PRINT_LEVELV_NUM, msg, args, **kwargs)


logging.Logger.print = printlog

T_VERBOSITY = Dict[str, Union[int, logging.Formatter]]
VERBOSITIES = (
    dict(
        level=logging.INFO,
        fmt=logging.Formatter(
            '%(asctime)s - %(name)s'
            '-%(funcName)s()'
            ': %(message)s'
        )
    ),
    dict(
        level=logging.INFO,
        fmt=logging.Formatter(
            '%(asctime)s - %(filename)s'
            '-%(funcName)s()'
            '-%(levelname)s: %(message)s'
        )
    ),
    dict(
        level=logging.DEBUG,
        fmt=logging.Formatter(
            '%(asctime)s - %(filename)s'
            '-%(funcName)s()'
            '-%(levelname)s: %(message)s'
        ),
    ),
    dict(
        level=logging.DEBUG,
        fmt=logging.Formatter(
            '%(asctime)s - %(filename)s'
            ':%(lineno)s-%(funcName)s()'
            '-%(levelname)s: %(message)s'
        ),
    ),
    dict(
        level=logging.DEBUG,
        fmt=logging.Formatter(
            '%(asctime)s - '
            'P=%(processName)s-T='
            '%(threadName)s'
            '-%(filename)s'
            ':%(lineno)s-%(funcName)s()'
            '-%(levelname)s: %(message)s'
        ),
    ),
    dict(
        level=logging.DEBUG,
        fmt=logging.Formatter(
            '%(asctime)s - '
            'P=%(processName)s(%(process)d)'
            '-T=%(threadName)s(%(thread)d)'
            '-%(filename)s'
            ':%(lineno)s-%(funcName)s()'
            '-%(levelname)s: %(message)s'
        ),
    ),
)


def get_loggers(name: str)->Tuple[logging.Logger, logging.Logger, logging.StreamHandler]:
    logger = logging.getLogger(name)
    logger_both = logging.getLogger(name + '-both')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    logger_both.addHandler(stdout_handler)
    return logger, logger_both, stdout_handler


def config_loggers(verbose: int, handlers: List[logging.Handler]):
    if logging.root.hasHandlers():
        root_stderr_handler = logging.root.handlers[0]
    else:
        root_stderr_handler = logging.StreamHandler()
        logging.root.addHandler(root_stderr_handler)
    if verbose:
        _vb = verbose - 1 if verbose < len(VERBOSITIES) else -1
        logging.root.setLevel(VERBOSITIES[_vb]['level'])
        root_stderr_handler.setFormatter(VERBOSITIES[_vb]['fmt'])
        for _handler in handlers:
            _handler.setFormatter(VERBOSITIES[_vb]['fmt'])
