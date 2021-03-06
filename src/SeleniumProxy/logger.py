import logging
import os.path
from functools import lru_cache
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

try:
    location = BuiltIn().get_variable_value("${OUTPUT DIR}")
    robot_log_level = BuiltIn().get_variable_value("${LOG LEVEL}")
except RobotNotRunningError:
    location = "."
    robot_log_level = "INFO"

log_name = os.path.join(location, "{}.log".format("SeleniumProxy"))
log_handler = logging.FileHandler(log_name)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log_handler.setFormatter(formatter)
LEVELS = {"FAIL": logging.DEBUG, "WARN": logging.warn,
          "INFO": logging.INFO, "DEBUG": logging.debug, "TRACE": logging.DEBUG}


@lru_cache(maxsize=1)
def get_logger(name):
    lgr = logging.getLogger(name)
    lgr.addHandler(log_handler)
    set_to = LEVELS[robot_log_level]
    lgr.setLevel(set_to)  # type: ignore
    lgr.debug(" **** New Session Created for {}  **** ".format(name))
    return lgr


def kwargstr(kwargs):
    return ", ".join("%s=%r" % x for x in kwargs.items())


def argstr(args):
    return ", ".join("%s" % x for x in args)
