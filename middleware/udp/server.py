import threading
import socketserver


class Handler(object):

    def __init__(self):
        self.__client_address = None
        self.__request = None

    def handle(self, server=None):
        pass

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request):
        self.__request = request

    @property
    def client_address(self):
        return self.__client_address

    @client_address.setter
    def client_address(self, client_address):
        self.__client_address = client_address


class SimpleHandler(Handler):

    def handle(self, server=None, handler=None):
        # example handling
        data = self.request[0].strip()
        socket = self.request[1]
        thread = threading.current_thread()
        print("In thread: {} ({})".format(thread.name, type(server)))
        print("Received: {}, returning: {}".format(data, data.upper()))
        socket.sendto(data.upper(), self.client_address)


class ManagedHandler(Handler):

    def handle(self, server=None, handler=None, manager=None):
        try:
            manager.request = self.request
            manager.client_address = self.client_address
        except (BaseException, ):
            raise Exception("Managed handlers expect Manager instance, {} encountered".format(type(manager)))
        return manager.manage(self.request)


class ThreadedUDPHandler(socketserver.BaseRequestHandler):

    BUFFER_LENGTH = 1024
    ENCODING = 'utf-8'

    def handle(self, server=None, handler=None, manager=None):
        handler.request = self.request
        handler.client_address = self.client_address
        handler.handle(manager=manager)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


class Server(object):

    DEFAULT_HOST = "0.0.0.0"
    DEFAULT_PORT = 12345

    def __init__(self, host=None, port=None):
        self.server = None
        self.host = self.DEFAULT_HOST
        self.port = self.DEFAULT_PORT
        if host is not None and port is not None:
            self.setup(host=host, port=port)

    def setup(self, host=None, port=None):
        if host is not None:
            self.host = host
        if port is not None:
            self.port = port

    def run(self, instance=None, handler=None, manager=None):

        if isinstance(instance, ThreadedUDPServer):
            self.server = instance
        else:
            class ThreadedUDPHandlerWithServer(ThreadedUDPHandler):

                def handle(self, _server=None, _handler=None, _manager=None):
                    super().handle(server=instance, handler=handler, manager=manager)
            self.server = ThreadedUDPServer((self.host, self.port), ThreadedUDPHandlerWithServer)

        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        print("Server started, single server instance up and running on {}".format(server_thread.name))

        self.server.serve_forever()

    def stop(self):

        self.server.shutdown()
        self.server.server_close()


if __name__ == "__main__":

    def print_handler(payload=None):
        print(payload)
        return True

    # # # simple handler
    # demo_server = Server()
    # demo_handler = SimpleHandler()
    # demo_server.run(handler=demo_handler)

    # # # managed handler
    from dna.middleware.models.manager import *

    demo_handler = ManagedHandler()
    demo_manager = Manager()
    demo_manager.add(entity='resource', _id=257, handler=print_handler)
    demo_server = Server()
    demo_server.run(handler=demo_handler, manager=demo_manager)
