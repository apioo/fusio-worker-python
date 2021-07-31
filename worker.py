import os.path
import sys
import json
import importlib
import http.client
from MySQLdb import _mysql

sys.path.append("./actions")
sys.path.append("./worker")

from worker import Worker
from worker.ttypes import Message, Result, Event, Log, Response

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class WorkerHandler:
    def __init__(self):
        self.connections = None

    def setConnection(self, connection):
        file = './connections.json'
        data = self.readConnections()

        if not connection.name:
            return Message(success=False, message='Provided no connection name')

        data[connection.name] = {
            'type': connection.type,
            'config': connection.config,
        }

        handle = open(file, "a")
        handle.write(json.dumps(data))
        handle.close()

        self.connections = None

        print('Update connection ' + connection.name)

        return Message(success=True, message='Update connection successful')

    def setAction(self, action):
        dir = './action'
        if not os.path.isdir(dir):
            os.mkdir(dir)

        if not action.name:
            return Message(success=False, message='Provided no action name')

        file = dir + '/' + action.name + '.js'

        handle = open(file, "a")
        handle.write(action.code)
        handle.close()

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

        file = './connections.json'
        if os.path.isfile(file):
            with open(file) as json_file:
                self.connections = json.load(json_file)

        if self.connections is not None:
            return self.connections

        return {}


class Connector:
    def __init__(self, connections):
        self.connections = connections
        self.instances = {}

    def getConnection(self, name):
        if self.instances[name]:
            return self.instances[name]

        if not self.connections[name]:
            raise Exception("Provided connection is not configured")

        connection = self.connections[name]

        if connection.type == "Fusio.Adapter.Sql.Connection.Sql":
            if connection.config.type == "pdo_mysql":
                con = _mysql.connect(
                    connection.config.host,
                    connection.config.username,
                    connection.config.password,
                    connection.config.database
                )

                self.instances[name] = con

                return con
            else:
                raise Exception("SQL type is not supported")
        elif connection.type == "Fusio.Adapter.Sql.Connection.SqlAdvanced":
            # TODO

            return None
        elif connection.type == "Fusio.Adapter.Http.Connection.Http":
            client = http.client.HTTPConnection(connection.config.url)

            # @TODO configure proxy for http client
            #connection.getConfig().get("username");
            #connection.getConfig().get("password");
            #connection.getConfig().get("proxy");

            self.instances[name] = client

            return client;
        else:
            raise Exception("Provided a not supported connection type");


class Dispatcher:
    def __init__(self):
        self.events = []

    def dispatch(self, eventName, data):
        self.events.append(Event(eventName, data))

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
        return Response(statusCode, headers, body)


if __name__ == '__main__':
    handler = WorkerHandler()
    processor = Worker.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9093)
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
