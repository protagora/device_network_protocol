import re
from dna.middleware.endpoint.client import Client


class ProtocolException(Exception):
    pass


class Router(object):

    @staticmethod
    def route(address=None):
        try:
            return address >> 4*8 & 2**16-1, address >> 2*8 & 2**16-1, address & 2**16-1
        except (BaseException, ):
            raise Exception("Address could not be routed")


class Parser(object):

    TEMPLATE = [
        {
            'id': 2
        }, {
            'flags': 2
        }, {
            'request_address': 6
        }, {
            'response_address': 6
        }, {
            'data_window_start': 6
        }, {
            'data_window_end': 6
        }, {
            'payload': 0
        }
    ]

    def parse(self, data=None):
        parts = dict()
        total = 0
        for item in self.TEMPLATE:
            key = None
            for key, length in item.items():
                pass
            merged = 0
            if length == 0:
                parts[key] = data[total:]
                return parts
            for byte in range(length):
                try:
                    merged <<= 8
                    merged |= data[total]
                except (BaseException, ):
                    merged |= 0
                total += 1
            parts[key] = merged
        return parts

    def pack(self, packet=None):
        response = list()
        for item in self.TEMPLATE:
            key, length = None, None
            for key, length in item.items():
                pass
            value = getattr(packet, key)
            if not value:
                value = 0
            partial = list()
            if 'payload' == key:
                partial = packet.payload
            else:
                if 'flags' == key:
                    value = value.pack()
                for byte in range(length):
                    partial.append(value >> byte * 8 & 2**8-1)
                partial = reversed(partial)
            response.extend(partial)
        return bytes(response)


class Flags(object):

    """
    # TYPE_REQUEST = 0
    # TYPE_RESPONSE = 1
    #
    # TARGET_SERVICE = 0
    # TARGET_DEVICE = 1
    #
    # ACTION_READ = 0
    # ACTION_WRITE = 1
    #
    # RESPONSE_NOT_REQUIRED = 0
    # RESPONSE_REQUIRED = 1
    #
    # WINDOW_NOT_SUPPORTED = 0
    # WINDOW_SUPPORTED = 1
    #
    # CONFIG_CONFIG = 0
    # CONFIG_MESSAGE = 1
    #
    # INIT_FALSE = 0
    # INIT_TRUE = 1
    """

    FLAGS_WIDTH = 16

    FIELDS = [
            'type',
            'flow_control',
            'target',
            'action',
            'response_required',
            'window',
            'config',
            'init'
        ]

    def __init__(self, flags=None):
        self.__type = None
        self.__flow_control = None
        self.__target = None
        self.__action = None
        self.__response_required = None
        self.__window = None
        self.__config = None
        self.__init = None
        self._setup(flags=flags)

    def __repr__(self):
        return ', '.join([str(i) for i in self.fields()])

    def __unicode__(self):
        return ', '.join([str(i) for i in self.fields()])

    def _setup(self, flags=None):
        try:
            self.unpack(flags=flags)
        except (BaseException, ):
            raise

    def _options(self, options=None):
        pass

    def fields(self):
        return {field: int(not not getattr(self, field)) for field in self.FIELDS}

    def pack(self):
        packed = int(self.type)
        for item in self.FIELDS[1:]:
            try:
                packed = packed << 1 | int(getattr(self, item))
            except (BaseException, ):
                packed <<= 1
        packed <<= self.FLAGS_WIDTH - len(self.FIELDS)
        return packed

    def unpack(self, flags=None):
        try:
            assert isinstance(flags, int)
        except (BaseException, ):
            raise ProtocolException("Flags expect an integer for unpacking")
        try:
            assert 0 <= flags < 2**16
        except:
            raise ProtocolException("Flags field value out of boundaries [{} - {}]]".format(0, 2**16-1))
        for index, field in enumerate(self.FIELDS):
            try:
                value = int(flags >> (self.FLAGS_WIDTH - index - 1) & 1)
                setattr(self, field, value)
            except (BaseException, ):
                setattr(self, field, 0)

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, _type):
        self.__type = _type

    @property
    def flow_control(self):
        return self.__flow_control

    @flow_control.setter
    def flow_control(self, flow_control):
        self.__flow_control = flow_control

    @property
    def target(self):
        return self.__target

    @target.setter
    def target(self, target):
        self.__target = target

    @property
    def action(self):
        return self.__action

    @action.setter
    def action(self, action):
        self.__action = action

    @property
    def response_required(self):
        return self.__response_required

    @response_required.setter
    def response_required(self, response_required):
        self.__response_required = response_required

    @property
    def window(self):
        return self.__window

    @window.setter
    def window(self, window):
        self.__window = window

    @property
    def config(self):
        return self.__config

    @config.setter
    def config(self, config):
        self.__config = config

    @property
    def init(self):
        return self.__init

    @init.setter
    def init(self, init):
        self.__init = init


class Packet(object):

    """
    DNP data container
    """

    ERROR_DATA_NONE = "Packet data must not be None"
    ERROR_MISSING_ID = "Packed missing mandatory field: ID"
    ERROR_MISSING_FLAGS = "Packed missing mandatory field: flags"

    FIELDS = [
        'id',
        'flags',
        'request_address',
        'response_address',
        'data_window_start',
        'data_window_end',
        'payload'
    ]

    def __init__(self, packet=None):
        """
        :param packet: dictionary of required and optional fields, see self.FIELDS for reference
        :return: None
        """
        self.__id = None
        self.__flags = None
        self.__request_address = None
        self.__response_address = None
        self.__data_window_start = None
        self.__data_window_end = None
        self.__payload = None
        self._setup(packet=packet)
        return None

    def __repr__(self):
        return str(self.id)

    def __unicode__(self):
        return str(self.id)

    def _setup(self, packet=None):
        try:
            assert packet is not None
        except (BaseException, ):
            raise ProtocolException(self.ERROR_DATA_NONE)
        try:
            self.id = packet['id']
        except (BaseException, ):
            raise ProtocolException(self.ERROR_MISSING_ID)
        try:
            flags = Flags(packet['flags'])
            self.flags = flags
        except (BaseException, ):
            raise ProtocolException(self.ERROR_MISSING_FLAGS)
        self._options(packet=packet)

    def _options(self, packet=None):
        if 'request_address' in packet.keys():
            self.request_address = packet['request_address']
        if 'response_address' in packet.keys():
            self.response_address = packet['response_address']
        if 'data_window_start' in packet.keys():
            self.data_window_start = packet['data_window_start']
        if 'data_window_end' in packet.keys():
            self.data_window_end = packet['data_window_end']
        if 'payload' in packet.keys():
            self.payload = packet['payload']

    def pack(self):
        parser = Parser()
        return parser.pack(self)

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, _id=None):
        self.__id = _id

    @property
    def flags(self):
        return self.__flags

    @flags.setter
    def flags(self, flags=None):
        try:
            assert isinstance(flags, Flags)
            self.__flags = flags
        except:
            raise ProtocolException("Flags must be an instance of Flags")

    @property
    def request_address(self):
        return self.__request_address

    @request_address.setter
    def request_address(self, request_address):
        self.__request_address = request_address

    @property
    def response_address(self):
        return self.__response_address

    @response_address.setter
    def response_address(self, response_address):
        self.__response_address = response_address

    @property
    def data_window_start(self):
        return self.__data_window_start

    @data_window_start.setter
    def data_window_start(self, data_window_start):
        self.__data_window_start = data_window_start

    @property
    def data_window_end(self):
        return self.__data_window_end

    @data_window_end.setter
    def data_window_end(self, data_window_end):
        self.__data_window_end = data_window_end

    @property
    def payload(self):
        return self.__payload

    @payload.setter
    def payload(self, payload):
        self.__payload = payload


class Transport(object):

    def __init__(self, client=None):
        self.__client = None
        self.__flags = None
        self.__packet = None
        self.__ip = None
        self.__port = None
        self._setup(client=client)

    def _setup(self, client=None):
        self.client = client
        if self.client is None:
            self.client = Client()

    def send(self, packet=None, ip=None, port=None):
        try:
            assert isinstance(packet, Packet)
            self.packet = packet
        except (BaseException, ):
            raise ProtocolException("Transport expects Packet instance for sending")
        try:
            self.ip = str(ip)
        except (BaseException, ):
            raise ProtocolException("IP address must be a string")
        try:
            self.port = int(port)
        except (BaseException, ):
            raise ProtocolException("Port number must be an integer")
        self._send()

    def receive(self, data=None):
        parser = Parser()
        parsed = parser.parse(data=data)
        self.packet = Packet(parsed)
        return self.packet

    def _send(self):
        self.verify()
        self.client.send(ip=self.ip, port=self.port, message=self.packet.pack())

    def verify(self):
        pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
        if not pattern.match(self.ip):
            raise ProtocolException("IP address not valid")
        if not 0 < self.port < 2**16:
            raise ProtocolException("Port number out of range")

    @property
    def client(self):
        return self.__client

    @client.setter
    def client(self, client):
        try:
            assert isinstance(client, Client)
            self.__client = Client
        except (BaseException, ):
            raise ProtocolException("Transport expects a Client instance, {} encountered".format(type(client)))

    @property
    def flags(self):
        return self.__flags

    @flags.setter
    def flags(self, flags):
        self.__flags = flags

    @property
    def packet(self):
        return self.__packet

    @packet.setter
    def packet(self, packet):
        self.__packet = packet

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, ip):
        self.__ip = ip

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port


if "__main__" == __name__:

    # # flags test
    # _flags = Flags(flags=2 ** 10 + 2 ** 9)
    # print(_flags.fields())
    # print(_flags.pack())
    # print(_flags)
    #
    # # packet test
    # data = {
    #     'id': 30000,
    #     'flags': _flags,
    #     'type': 1
    # }
    # _packet = Packet(packet=data)
    # print(_packet.flags.fields())
    # print(_packet)

    # parser
    print('--- Parser test ---')
    _data = [254, 2, 255, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 8, 9, 0, 1, 2, 3,
             4, 5, 6, 7, 8, 9]
    _parser = Parser()
    _parsed = _parser.parse(_data)
    print(_parsed)

    # parsed_flags = Flags(parsed['flags'])
    # parsed['flags'] = parsed_flags
    _packet = Packet(packet=_parsed)
    print(_packet.flags.fields())
    print(_data)
    # print(bytes(_packet.pack()))
    print(_packet.pack())
    print(''.join([str(item) for item in _packet.pack()]).encode('ascii'))
    # _flags.unpack(parsed['flags'])
    # print(_flags.fields())

    # router
    print('--- Router test ---')
    print(Router.route(2**47+2**27+2**9))
