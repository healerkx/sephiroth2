
import logging
from logging import handlers
# from defines import *

class Logger:
    """
    """

    #日志级别关系映射
    level_relations = {
        'debug':    logging.DEBUG,
        'info':     logging.INFO,
        'warning':  logging.WARNING,
        'error':    logging.ERROR,
        'crit':     logging.CRITICAL
    }

    def __init__(self, filename, level="info"):
        self.__logger = logging.getLogger(filename)
        #设置日志格式
        formatter = logging.Formatter(Logger_Format)
        #设置日志级别
        self.__logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()    #往屏幕上输出
        sh.setFormatter(formatter)      #设置屏幕上显示的格式
        #往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(
            filename=filename, when='D', backupCount=1, encoding='utf-8')
        
        th.setFormatter(formatter)
        self.__logger.addHandler(sh)
        self.__logger.addHandler(th)

    def get_logger(self):
        return self.__logger