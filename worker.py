import http.client
import importlib
import json
import os.path
import sys
import traceback
import pymysql.cursors

sys.path.append("./actions")
sys.path.append("./worker")

from worker import Worker
from worker.ttypes import Message, Result, Event, Log, Response

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class WorkerHandler:
    ACTIONS_DIR = './actions'

    def __init__(self):
        self.connections = None

    def setConnection(self, connection):
        if not os.path.isdir(self.ACTIONS_DIR):
            os.mkdir(self.ACTIONS_DIR)

        data = self.readConnections()

        if not connection.name:
            return Message(success=False, message='Provided no connection name')

        data[connection.name] = {
            'type': connection.type,
            'config': connection.config,
        }

        with open(self.ACTIONS_DIR + '/connections.json', 'w') as connection_file:
            connection_file.seek(0)
            connection_file.write(json.dumps(data))
            connection_file.truncate()

        self.connections = None

        print('Update connection ' + connection.name)

        return Message(success=True, message='Update connection successful')

    def setAction(self, action):
        if not os.path.isdir(self.ACTIONS_DIR):
            os.mkdir(self.ACTIONS_DIR)

        if not action.name:
            return Message(success=False, message='Provided no action name')

        file = self.ACTIONS_DIR + '/' + action.name + '.py'

        with open(file, 'w') as action_file:
            action_file.seek(0)
            action_file.write(action.code)
            action_file.truncate()

        sys.modules.clear()

        print('Update action ' + action.name)

        return Message(success=True, message='Update action successful')

    def executeAction(self, execute):
        connector = Connector(self.readConnections())
        dispatcher = Dispatcher()
        logger = Logger()
        responseBuilder = ResponseBuilder()

        if not execute.action:
            return

        print('Execute action ' + execute.action)

        try:
            module = importlib.import_module(execute.action)

            response = module.handle(execute.request, execute.context, connector, responseBuilder, dispatcher, logger)

            return Result(response, dispatcher.getEvents(), logger.getLogs())
        except Exception as e:
            return Result(Response(500, None, json.dumps({
                'success': False,
                'message': 'An error occurred at the worker: ' + str(e),
            })))

    def readConnections(self):
        if self.connections is not None:
            return self.connections

        file = self.ACTIONS_DIR + '/connections.json'
        if os.path.isfile(file):
            with open(file) as json_file:
                self.connections = json.load(json_file)

        if self.connections is not None:
            return self.connections

        return {}


class Connector:
    def __init__(self, configs):
        self.configs = configs
        self.connections = {}

    def getConnection(self, name):
        if name in self.connections.keys():
            return self.connections[name]

        if name not in self.configs.keys():
            raise Exception("Provided connection is not configured")

        config = self.configs[name]

        if config['type'] == "Fusio.Adapter.Sql.Connection.Sql":
            if config['config']['type'] == "pdo_mysql":
                con = pymysql.connect(
                    host=config['config']['host'],
                    user=config['config']['username'],
                    password=config['config']['password'],
                    database=config['config']['database']
                )

                self.connections[name] = con

                return con
            else:
                raise Exception("SQL type is not supported")
        elif config['type'] == "Fusio.Adapter.Sql.Connection.SqlAdvanced":
            # TODO

            return None
        elif config['type'] == "Fusio.Adapter.Http.Connection.Http":
            client = http.client.HTTPConnection(config['config']['url'])

            # @TODO configure proxy for http client
            #config['config']['username']
            #config['config']['password']
            #config['config']['proxy']

            self.connections[name] = client

            return client
        else:
            raise Exception("Provided a not supported connection type")


class Dispatcher:
    def __init__(self):
        self.events = []

    def dispatch(self, eventName, data):
        self.events.append(Event(eventName, json.dumps(data)))

    def getEvents(self):
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
        self.logs.append(Log(level, message))

    def getLogs(self):
        return self.logs


class ResponseBuilder:
    def build(self, statusCode, headers, body):
        return Response(statusCode, headers, json.dumps(body))


if __name__ == '__main__':
    handler = WorkerHandler()
    processor = Worker.Processor(handler)
    transport = TSocket.TServerSocket(host='localhost', port=9093)
    transportFactory = TTransport.TBufferedTransportFactory()
    protocolFactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, transportFactory, protocolFactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print('Started Fusio worker')
    server.serve()
