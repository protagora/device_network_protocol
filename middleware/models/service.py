from dna.middleware.models.manager import *
from dna.middleware.endpoint.server import ManagedHandler
from dna.middleware.endpoint.server import Server


class Service(object):

    def __init__(self, host=None, port=None):
        self.__manager = None
        self.__server = None
        self.__host = None
        self.__port = None
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

    def run(self):

        def print_handler(payload=None):
            print(payload)
            return True

        # # # managed handler
        # @todo: replace using local managed handler with provided handler
        # @todo: if no default handler is provided as a parameter to call

        demo_handler = ManagedHandler()
        demo_manager = Manager()
        demo_manager.add(entity='resource', _id=257, handler=print_handler)
        demo_server = Server(host=self.host, port=self.port)
        demo_server.run(handler=demo_handler, manager=demo_manager)

    @property
    def manager(self):
        return self.__manager

    @manager.setter
    def manager(self, manager):
        try:
            assert isinstance(manager, Manager)
        except (BaseException, ):
            raise Exception("Manager instance expected, {} encountered".format(type(manager)))
        self.__manager = manager
        manager.service = self

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server):
        try:
            assert isinstance(server, Server)
        except (BaseException, ):
            raise Exception("Server instance expected, {} encountered".format(type(server)))
        self.__server = server
        server.service = self

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, host):
        self.__host = host

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port
