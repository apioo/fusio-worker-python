import os.path
import re
import sys

from runtime.generated.execute import Execute
from runtime.generated.message import Message
from runtime.generated.update import Update
from runtime.runtime import Runtime


class Worker:
    ACTIONS_DIR = './actions'

    def __init__(self):
        self.runtime = Runtime()

    def get(self):
        return self.runtime.get()

    def execute(self, action: str, execute: Execute):
        self.assert_action(action)

        return self.runtime.run(action, execute)

    def put(self, action: str, update: Update):
        if not os.path.isdir(self.ACTIONS_DIR):
            os.mkdir(self.ACTIONS_DIR)

        file = self.get_action_file(action)
        code = update.code

        with open(file, 'w') as action_file:
            action_file.seek(0)
            action_file.write(code)
            action_file.truncate()

        self.clear_cache()

        return self.new_message(True, "Action successfully updated")

    def delete(self, action: str) -> Message:
        if not os.path.isdir(self.ACTIONS_DIR):
            os.mkdir(self.ACTIONS_DIR)

        file = self.get_action_file(action)

        os.remove(file)

        self.clear_cache()

        return self.new_message(True, "Action successfully deleted")

    def get_action_file(self, action: str) -> str:
        self.assert_action(action)

        return self.ACTIONS_DIR + '/' + action + '.py'

    def assert_action(self, action: str):
        if not re.match("^[A-Za-z0-9_-]{3,30}$", action):
            raise Exception("Provided no valid action name: " + action)

    def new_message(self, success: bool, message: str) -> Message:
        result = Message()
        result.success = success
        result.message = message
        return result

    def clear_cache(self):
        sys.modules.clear()
