





class Action:
    '''
    一个Action表达一个被执行的动作，在config文件中被以字符串的形式指明。
    通常来说，一个进程内的Action都是prototype的实例，而不是Singleton实例。
    即每次执行会创建一个新的Action实例，被Executor创建，加载，执行。
    '''
    def __init__(self):
        pass

    @staticmethod
    def get_action_class(action_type):
        if action_type in Action.action_classes:
            return Action.action_classes[action_type]
        raise Exception(f"No action named '{action_type}' register")

    ##
    # Register
    """
    Hold the registered class object
    """
    action_classes = dict()

    #
    @staticmethod
    def register(action_type):
        """
        Create a derived-action-class instance should use get_action_class()
        """
        def action_class(action_clz):
            Action.action_classes[action_type] = action_clz
        return action_class        

    def set_info(self, action_name, config):
        self.action_name = action_name
        self.config = config


    def try_execute(self, context):
        '''
        先走基类的try_execute, 派生类需要提供execute(context)方法
        '''
        self.context = context
        self.execute(context)

        current_action_config_exit_at = f"action.{self.action_name}.exit_at"
        exit_at = self.config.get_value(current_action_config_exit_at)
        print("exit_at", exit_at)
        if exit_at:
            expr = context.evaluate(exit_at)
            # If the express returns True, 
            # throw Exception to finish the whole execution of the pipeline.
            if eval(expr):
                raise Exception("exit at %s" % exit_at)

        self.context = None

    def execute(self, context):
        raise Exception("Sub-Action class should implement this method!")

@Action.register("example")
class ExampleAction(Action):
    def __init__(self):
        print("ExampleAction::__init__(self)")

    def execute(self, context):
        print(f"ExampleAction::execute(self, {context})")

