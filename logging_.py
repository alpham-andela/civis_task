"""
Configure custom logger to
add colorized output on the console
"""
import copy
import logging
import configs

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

# The background is set with 40 plus the number of the color, and the foreground with 30

# These are the sequences needed to get colored output
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"


def formatter_message(message, use_color=True):
    """
    Methods creates a message format
    :param message:
    :param use_color:
    :return:
    """
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message


COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}


class ColoredFormatter(logging.Formatter):
    """
    Custom message formatter
    """

    def __init__(self, msg, use_color=True):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color

    def format(self, record):
        """
        Override to the parents format method
        :param record:
        :return:
        """
        record = copy.copy(record)

        levelname = record.levelname
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            record.levelname = levelname_color
        return logging.Formatter.format(self, record)


# Custom logger class with multiple destinations
class ColoredLogger(logging.Logger):
    """
    Custom logger to replace the default logger
    """
    FORMAT = configs.LOG_FORMAT
    FORMAT_FILE = configs.LOG_FORMAT_FILE

    COLOR_FORMAT = formatter_message(FORMAT, True)

    def __init__(self, name):
        if configs.DEBUG:
            logging.Logger.__init__(self, name, logging.DEBUG)
        else:
            logging.Logger.__init__(self, name, logging.INFO)

        color_formatter = ColoredFormatter(self.COLOR_FORMAT)
        file_formatter = logging.Formatter(self.FORMAT_FILE)

        console = logging.StreamHandler()
        logfile = logging.FileHandler(configs.LOG_FILE)

        console.setFormatter(color_formatter)
        logfile.setFormatter(file_formatter)

        self.addHandler(console)
        self.addHandler(logfile)


logging.setLoggerClass(ColoredLogger)
