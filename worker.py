import base64
import http.client
import importlib
import json
import os.path
import re
import sys
from typing import Dict
from urllib.parse import urlparse

import psycopg2
import pymysql.cursors
from elasticsearch import Elasticsearch
from pymongo import MongoClient

from generated.about import About
from generated.execute import Execute
from generated.execute_connection import ExecuteConnection
from generated.message import Message
from generated.response import Response
from generated.response_event import ResponseEvent
from generated.response_http import ResponseHTTP
from generated.response_log import ResponseLog
from generated.update import Update


class Worker:
    ACTIONS_DIR = './actions'

    def get(self):
        about = About()
        about.api_version = "1.0.0"
        about.language = "python"
        return about

    def execute(self, action: str, execute: Execute):
        connector = Connector(execute.connections)
        dispatcher = Dispatcher()
        logger = Logger()
        response_builder = ResponseBuilder()

        self.assert_action(action)

        module = importlib.import_module(action, package=__name__)

        module.handle(execute.request, execute.context, connector, response_builder, dispatcher, logger)

        response = response_builder.get_response()
        if not response:
            response = ResponseHTTP()
            response.status_code = 204

        result = Response()
        result.response = response
        result.events = dispatcher.get_events()
        result.logs = logger.get_logs()
        return result

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


class Connector:
    def __init__(self, configs: Dict[str, ExecuteConnection]):
        self.configs = configs
        self.connections = {}

    def get_connection(self, name):
        if name in self.connections.keys():
            return self.connections[name]

        if name not in self.configs.keys():
            raise Exception("Provided connection is not configured")

        connection = self.configs[name]
        config = json.loads(base64.b64decode(connection.config))

        if connection.type == "Fusio.Adapter.Sql.Connection.Sql":
            if config['type'] == "pdo_mysql":
                con = pymysql.connect(
                    host=config['host'],
                    user=config['username'],
                    password=config['password'],
                    database=config['database']
                )
            elif config['type'] == "pdo_pgsql":
                con = psycopg2.connect(
                    host=config['host'],
                    database=config['database'],
                    user=config['username'],
                    password=config['password']
                )
            else:
                raise Exception("SQL type is not supported")

            self.connections[name] = con

            return con
        elif connection.type == "Fusio.Adapter.Sql.Connection.SqlAdvanced":
            # TODO

            return None
        elif connection.type == "Fusio.Adapter.Http.Connection.Http":
            url = urlparse(config['url'])
            scheme = "{0.scheme}".format(url)
            host = "{0.hostname}".format(url)
            port = url.port

            if not host:
                raise Exception("No hostname provided")

            if scheme == 'http':
                client = http.client.HTTPConnection(host, port)
            elif scheme == 'https':
                client = http.client.HTTPSConnection(host, port)
            else:
                raise Exception("Connection url provided an invalid scheme, supported is only http and https")

            # @TODO configure proxy for http client
            # config['username']
            # config['password']
            # config['proxy']

            self.connections[name] = client

            return client
        elif connection.type == "Fusio.Adapter.Mongodb.Connection.MongoDB":
            client = MongoClient(config['url'])
            database = client[config['database']]

            self.connections[name] = database

            return database
        elif connection.type == "Fusio.Adapter.Elasticsearch.Connection.Elasticsearch":
            host = config['host']
            client = Elasticsearch(host.split(','))

            self.connections[name] = client

            return client
        else:
            raise Exception("Provided a not supported connection type")


class Dispatcher:
    def __init__(self):
        self.events = []

    def dispatch(self, event_name, data):
        event = ResponseEvent()
        event.event_name = event_name
        event.data = data
        self.events.append(event)

    def get_events(self):
        return self.events


class Logger:
    def __init__(self):
        self.logs = []

    def emergency(self, message):
        self.log("EMERGENCY", message)

    def alert(self, message):
        self.log("ALERT", message)

    def critical(self, message):
        self.log("CRITICAL", message)

    def error(self, message):
        self.log("ERROR", message)

    def warning(self, message):
        self.log("WARNING", message)

    def notice(self, message):
        self.log("NOTICE", message)

    def info(self, message):
        self.log("INFO", message)

    def debug(self, message):
        self.log("DEBUG", message)

    def log(self, level, message):
        log = ResponseLog()
        log.level = level
        log.message = message
        self.logs.append(log)

    def get_logs(self):
        return self.logs


class ResponseBuilder:
    def __init__(self):
        self.response = None

    def build(self, status_code, headers, body):
        self.response = ResponseHTTP()
        self.response.status_code = status_code
        self.response.headers = headers
        self.response.body = body

    def get_response(self):
        return self.response
