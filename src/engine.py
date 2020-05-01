
import threading
import traceback

try:
    '''
    Load All actions
    '''
    from actions import *
except:
    pass
#from resource import Resource
from context import *
#from actions import *
#from defines import *


class Engine:
    """
    An engine drives a sequence of actions with a context
    """
    
    def __init__(self, config):
        """
        param: 
        """
        self.config = config
        # run-actions times, 需要改名
        self.exec_times = 0
        self.trigger_time = 0
        self.name = ""#self.config['main']['name']
        self.__state = 0
        self.engine_instance_vars = dict()

        # Resource.initialize_local_resources(self.name, self.config)
    
    def __str__(self):
        return "%s@%d" % (self.name, self.__state)

    def get_state(self):
        return self.__state

    def run(self, context=None):
        """
        Run the actions, provide the context.
        """
        try:
            self.__state = 1
            print("ThreadId:", threading.get_ident())
            context = self.__run(context)
            
            print("Engine::run action")
        except Exception as e:
            print_exception = True # Resource.get_global_var('$print_exception')
            if print_exception == 1:
                print(traceback.format_exc())
            else:
                print("Exception:", e)
        finally:
            self.__state = 2
            # Keep the context for the follower engines

    def set_trigger_time(self, trigger_time):
        self.trigger_time = trigger_time

    # !
    def initialize_vars(self, vars):
        """
        """
        for key, value in vars.items():
            self.engine_instance_vars[key] = value

    def start(self):
        """
        """
        ...
        if 'vars' in self.config:
            self.initialize_vars(self.config['vars'])

        triggers = self.config['main']['triggers']
        if isinstance(triggers, str):
            triggers = [triggers]

        self.__state = EngineState_Start
        for trigger in triggers:
            pass
            # Clock.register(self, trigger)

    def __run(self, context):
        """
        """
        if not context:
            context = Context()

        # context.set_engine(self) # 是否需要?
        sequence = self.config.get_value("actions.sequence")

        print("sequence", sequence)
        for action_name in sequence:
            print("action_name", action_name)
            self.run_action(action_name, context)
        
        # final context?
        return context

    def __create_action(self, action_name, context):
        """
        Create an action with its config
        """
        action_type = self.config.get_value(f"action.{action_name}.type")
        print("ActionType", action_type)
        clz = Action.get_action_class(action_type)
        action = clz()
        action.set_info(action_name, self.config)
        return action

    def load_actions(self, actions_config):
        """
        Action.main would be the first action
        """
        actions = []

        action_config = actions_config['main']
        action_name = 'main'
        while action_config:
            action = self.create_action(action_name, action_config)
            actions.append(action)
            
            if 'next' not in action_config or action_config['next'] == '':
                break
            next_action = action_config['next']
            if next_action not in actions_config:
                raise Exception("No action provided " + next_action)
            
            action_name = next_action
            action_config = actions_config[action_name]

        return actions

    def run_action(self, action_name, context):
        """
        """
        print("aaaa", action_name)
        action = self.__create_action(action_name, context)
        print("aaaa", action)
        #if action.precheck():
        #    pass
        action.try_execute(context)
        self.exec_times += 1

    def get_value(self, key, default_value=None):
        """
        Get engine instance variable value
        """
        if key == 'trigger_time':
            return self.trigger_time

        if key in self.engine_instance_vars:
            return self.engine_instance_vars[key]
        else:
            return default_value

    def set_value(self, key, value):
        self.engine_instance_vars[key] = value

