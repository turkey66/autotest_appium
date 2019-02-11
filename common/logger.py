import logging
import os
import sys
import time


class Logger:
    def __init__(
            self,
            set_level="debug",
            console=True,
            formatter=logging.Formatter(fmt='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s', datefmt='%Y/%m/%d %H:%M:%S'),
            name=os.path.split(os.path.splitext(sys.argv[0])[0])[-1],
            file_name=time.strftime("%Y-%m-%d.log", time.localtime()),
            dir_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "log"),
    ):
        '''
            set_level： 设置日志的打印级别，默认为DEBUG
            name： 日志中将会打印的name，默认为运行程序的name
            file_name： 日志文件的名字，默认为当前时间（年-月-日.log）
            dir_path： 日志文件夹的路径，默认为logger.py同级目录中的log文件夹
            console： 是否在控制台打印，默认为True
        '''

        self.logger = logging.getLogger(name)

        if set_level.lower() == "critical":
            self.logger.setLevel(logging.CRITICAL)
        elif set_level.lower() == "error":
            self.logger.setLevel(logging.ERROR)
        elif set_level.lower() == "warning":
            self.logger.setLevel(logging.WARNING)
        elif set_level.lower() == "info":
            self.logger.setLevel(logging.INFO)
        elif set_level.lower() == "debug":
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.NOTSET)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        log_dir_path = os.path.join(dir_path, file_name)
        log_handler = logging.FileHandler(log_dir_path)
        log_handler.setFormatter(formatter)
        self.logger.addHandler(log_handler)

        if console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def addHandler(self, hdlr):
        self.logger.addHandler(hdlr)

    def removeHandler(self, hdlr):
        self.logger.removeHandler(hdlr)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        self.logger.log(level, msg, *args, **kwargs)


if __name__ == '__main__':
    logger = Logger()
    logger.info("ssssssss哈哈哈")

    try:
        result = 10 / 0
    except Exception:
        logger.error('Faild to get result', exc_info=True)
    logger.debug('Finished')