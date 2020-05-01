
from actions import *

@Action.register("http.get")
class HttpGetAction(Action):

    def __init__(self):
        pass

    def execute(self, context):
        print(f"HttpGetAction::execute(self, {context})")
