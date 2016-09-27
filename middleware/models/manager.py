from datetime import datetime
from dna.middleware.endpoint.server import Handler
from dna.middleware.protocol.transport import Packet, Router, Parser


class Manager(object):

    """
    Manager contains handlers for all entities in the system: services/devices, components and resources. It is
    responsible for handlers callback execution.
    """

    ENTITY = ['service', 'component', 'resource']
    DEFAULT_ENCODING = "utf-8"

    DEFAULT_SUCCESS_MESSAGE = 'success'
    DEFAULT_ERROR_MESSAGE = 'failure'
    # HTTP style status codes and response messages
    ERROR_TARGET_NOT_FOUND = "404 Not found"
    ERROR_HANDLING_REQUEST = "500 Server error"
    # ERROR_TARGET_NOT_FOUND = "Target device or service not found"
    # ERROR_HANDLING_REQUEST = "Error handling request"

    def __init__(self):
        self.__entities = dict()

    def add(self, entity=None, _id=None, handler=None):
        try:
            assert entity in self.ENTITY
        except (BaseException, ):
            raise Exception("Entity not supported: {}".format(str(entity)))
        try:
            assert hasattr(handler, "__call__") or (type(handler) and issubclass(handler.__class__, Handler))
        except (BaseException, ):
            raise Exception("Handler must be a callable or a Handler subclass")
        if entity not in self.entities.keys():
            self.entities[entity] = dict()
        self.entities[entity][_id] = handler

    def remove(self, entity=None, _id=None):
        if entity in self.entities.keys() and _id in self.entities[entity].keys():
            del self.entities[entity][_id]

    @property
    def entities(self):
        return self.__entities

    @entities.setter
    def entities(self, entities):
        self.__entities = entities

    def manage(self, request=None):
        socket = request[1]
        try:
            entity, _id, payload = self.route(request=request)
            print(entity, _id, payload)
        except (BaseException, ):
            socket.sendto(bytes(self.ERROR_TARGET_NOT_FOUND, self.DEFAULT_ENCODING), self.client_address)
            return
        try:
            response = self.dispatch(entity, _id, payload)
        except (BaseException, ):
            socket.sendto(bytes(self.ERROR_HANDLING_REQUEST, self.DEFAULT_ENCODING), self.client_address)
            return
        # @todo: replace message with response.__repr__
        if response is True:
            message = self.DEFAULT_SUCCESS_MESSAGE
            # message = str(response)
        else:
            message = self.DEFAULT_ERROR_MESSAGE
        if 7 == socket.sendto(bytes(message, self.DEFAULT_ENCODING), self.client_address):
            return True
        return False

    def route(self, request=None):
        try:
            parser = Parser()
            parsed = parser.parse(request[0])
            packet = Packet(parsed)
        except (BaseException, ):
            print ("[{}: {}] Data packet not well formed, dropping".format(datetime.now(), self.client_address))
            return
        target_id, component_id, resource_id = Router.route(packet.request_address)
        if 0 == target_id:
            raise Exception("Routing failed, target service/device address is 0")
        entity = self.ENTITY[0]
        _id = target_id
        if 0 != component_id:
            entity = self.ENTITY[1]
            _id = component_id
            if 0 != resource_id:
                entity = self.ENTITY[2]
                _id = resource_id
        return entity, _id, packet.payload

    def dispatch(self, entity=None, _id=None, payload=None):
        if hasattr(self.entities[entity][_id], "__call__"):
            response = self.entities[entity][_id]()
        else:
            response = self.entities[entity][_id].handle(payload)
        return response
