import os.path
import re

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
        return self.runtime.run(self.get_action_file(action), execute)

    def put(self, action: str, update: Update):
        if not os.path.isdir(self.ACTIONS_DIR):
            os.mkdir(self.ACTIONS_DIR)

        file = self.get_action_file(action)
        code = update.code

        with open(file, 'w') as action_file:
            action_file.seek(0)
            action_file.write(code)
            action_file.truncate()

        self.runtime.reload(file)

        return self.new_message(True, "Action successfully updated")

    def delete(self, action: str) -> Message:
        if not os.path.isdir(self.ACTIONS_DIR):
            os.mkdir(self.ACTIONS_DIR)

        file = self.get_action_file(action)

        os.remove(file)

        return self.new_message(True, "Action successfully deleted")

    def get_action_file(self, action: str) -> str:
        parts = action.split('@')
        name = parts[0]
        action_hash = parts[1] if len(parts) > 1 else None

        self.assert_action(name)
        if action_hash:
            self.assert_hash(action_hash)

        base_dir = os.path.join(self.ACTIONS_DIR, name)

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        if action_hash:
            return os.path.join(base_dir, f"{action_hash}.py")
        else:
            return os.path.join(base_dir, "main.py")

    def assert_action(self, action: str):
        if not re.match("^[A-Za-z0-9_-]{3,255}$", action):
            raise Exception("Provided no valid action name: " + action)

    def assert_hash(self, action_hash: str):
        if not re.match("^[A-Za-z0-9]{3,255}$", action_hash):
            raise Exception("Provided no valid action hash: " + action_hash)

    def new_message(self, success: bool, message: str) -> Message:
        result = Message()
        result.success = success
        result.message = message
        return result
