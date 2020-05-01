
from apscheduler.schedulers.blocking import BlockingScheduler
from config import Config, ConfigFacade as CF
import signal, sys


class Sched:
    """
    """
    def __init__(self, config, engine):
        self.config = config
        self.engine = engine
        # Use BlockingScheduler
        self.scheduler = BlockingScheduler()
        self.__logger = None
        self.executors = dict()

    def set_logger(self, logger):
        self.__logger = logger

    def get_logger(self):
        return self.__logger

    def start(self):
        # 优雅退出, 没那么多异常栈信息
        signal.signal(signal.SIGINT, Sched.__exit_handler)
        
        sequence = self.config.get_value("actions.sequence")
        # 
        if len(sequence) == 0:
            print("Wrong sequence length, bad config")
            exit(0)
        
        self.__add_job(sequence[0], "pipeline")
        self.__run()

    def on_run(self, args):
        # do it! 触发后立即执行engine
        # TODO: logger
        self.engine.run()

    
    def __add_job(self, start_action_name, pipeline):
        '''

        '''
        params = dict()
        params['func'] = getattr(self, "on_run")
        params['id'] = start_action_name
        # What to fill the args
        params['args'] = [start_action_name]

        # start_action = CF.get_actions(self.config)[0]

        # https://blog.csdn.net/somezz/article/details/83104368
        # keep the design simple, 
        # 不做过早封装, 在toml中直接可以采用apscheduler的配置
        params.update(self.config.get_value("actions.sched.params"))
        # 添加一个定时任务
        self.scheduler.add_job(**params)

    def __run(self):
        self.scheduler.start()

    @staticmethod
    def __exit_handler(signum, frame):
        """
        Quit all the threads when Ctrl+C
        """
        # logger.info("exit.<Ctrl+C>")
        sys.exit()        

