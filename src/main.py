

import sys, os

try:
    '''
    Load All actions
    '''
    from actions import *
except:
    pass

try:
    '''
    Load All resources
    '''
    from resources import *
except:
    pass


from config import Config
from sched import Sched
from engine import Engine
from logger import Logger

def load_actions():
    '''
    Load all the actions?
    '''
    pass

def load_resources():
    
    a = MySQLConnection()    
    

def main(config):
    # Engine的生命周期是整个进程的生命周期
    engine = Engine(config)

    scheduler = Sched(config, engine)
    scheduler.start()
    # 从actions里面开始遍历


def load_config():
    from usage import usage
    work_path = ""
    if len(sys.argv) == 1:
        print(usage.__doc__)
        exit(0)

    from optparse import OptionParser    
    parser = OptionParser()

    parser.add_option("-c", "--config", action="store", dest="toml", help="Provide the config file *.toml")

    options, args = parser.parse_args()

    if not options.toml:
        print("Please provide the main toml file.")
        print(usage.__doc__)
        exit(0)

    
    config = Config(options.toml)
    main(config)


if __name__ == "__main__":
    load_actions()
    load_resources()
    load_config()
    