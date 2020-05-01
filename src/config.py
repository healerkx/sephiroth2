


import toml as toml

from const import *
from actions import *
import os

class Config:
    '''
    Redefine the config, it's diff from sephiroth v1
    Config对象代表了一个Pipeline的全部配置，
    它可以通过requires进行包含，一个Config对象代表关联的几个toml文件的最终配置结果。
    ! Config对象应该只能用get_value来获取配置, 不应该再支持[]操作[sephv1似乎支持]
    '''
    def __init__(self, filename):
        """
        self.filename is the toml file for start
        """
        Config.check_file_exists(filename)
        abspath = os.path.abspath(filename)
        
        self.filename = os.path.basename(abspath)
        self.path = os.path.dirname(abspath)
        # 文件和decoded的dict结果的映射, 而不是最终的merged的结果
        self.tomls = dict()
        #目前看没有用
        # self.toml_files = [] 
        # 最终的合并结果
        self.toml_config = None
        self.__load_start_toml_file(self.filename)
        
    def __load_start_toml_file(self, filename):
        # 先Parse files
        self.__parse_toml_files([filename])
        # 再Load and merge
        self.toml_config = self.__load_toml_files()
        print(self.toml_config)

    #
    def __parse_toml_files(self, toml_files):
        """
        Parse the toml files, especially against the 'requires'
        假设支持多个文件都运行出现requires，就是嵌套include。
        """
        for toml_file in toml_files:
            toml_file_path = os.path.join(self.path, toml_file)
            if toml_file_path in self.tomls:
                # 避免循环依赖
                continue
            Config.check_file_exists(toml_file_path)

            # tomls hold all the configs parsed from toml file.
            try:
                toml_config = toml.load(toml_file_path)
                # print(toml_config)
            except toml.TomlDecodeError as e:
                print(e, f"toml file {toml_file_path} decoded failed.")
                exit(0)

            # 已经toml parsed的文件
            # self.toml_files.append(toml_file_path)
            self.tomls[toml_file_path] = toml_config
            
            if "requires" in toml_config:
                # 有"requires"就递归一下
                toml_files = toml_config["requires"]
                self.__parse_toml_files(toml_files)

    def __load_toml_files(self) -> dict:
        """
        是个简单的合并dict到result dict的过程
        """
        result = dict()
        for filename, config in self.tomls.items():
            # config = self.tomls[filename]
            self.__merge_dict(result, config)
        return result

    @staticmethod
    def __merge_dict(d1: dict, d2: dict):
        """
        Merge d2 into d1
        """
        for key, value in d2.items():
            if key == '__filename__':
                continue
            if key not in d1:
                d1[key] = value
            else:
                d1[key].update(value)

    def get_pipeline(self, start_action_name: str):
        pipeline = dict()
        actions_map = self.get_value('action')
        action_name = start_action_name
        while action_name:
            if action_name in pipeline:
                # loop actions NOT support now.
                break
            pipeline[action_name] = actions_map[action_name]
            action_name = self.get_value('action.%s.next' % action_name)
        
        return pipeline


    @staticmethod
    def get_start_action_name(pipeline: dict):
        for action_name, action in pipeline.items():
            if 'start_at' in action:
                return action_name
        return None

    @staticmethod
    def get_action_config(pipeline: dict, action_name: str) -> dict:
        if action_name in pipeline:
            return pipeline[action_name]
        else:
            return None

    def get_value(self, key, default_val=None):
        '''
        '''
        if "." not in key:
            # Optimize
            if key in self.toml_config:
                return self.toml_config[key]
            else:
                return default_val
        key_parts = key.split(".")
        return Config.__get_value(self.toml_config, key_parts, default_val)

    @staticmethod
    def __get_value(config_dict, key_parts, default_val):
        config = config_dict
        for key_part in key_parts:
            if key_part in config:
                config = config[key_part]
            else:
                return default_val
        return config

    @staticmethod
    def check_file_exists(filename):
        if not os.path.isfile(filename):
            print(f"<{filename}> is not exist")
            exit(0)


class ConfigFacade:

    
    @staticmethod
    def get_actions(config):
        return config['actions']    
    
    @staticmethod
    def get_sched(config):
        return config['sched'] 