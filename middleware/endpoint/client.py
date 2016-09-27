import socket
import sys
import time


class Client(object):
    """ UDP based client """

    DEFAULT_IP = "127.0.0.1"
    DEFAULT_PORT = 12345
    # alt: ascii
    # utf-8 usually works better
    DEFAULT_ENCODING = "utf-8"
    BUFFER_SIZE = 1024
    TIMEOUT = 5

    def __init__(self, socket_instance=None):
        if isinstance(socket_instance, socket.socket):
            self.socket = socket_instance
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(self.TIMEOUT)

    def send(self, message=None, ip=None, port=None, raw=True, encoding=None):
        if not ip:
            ip = self.DEFAULT_IP
        if not port:
            port = self.DEFAULT_PORT
        try:
            if raw is True:
                payload_length = self.socket.sendto(message, (ip, port))
            else:
                if encoding is None:
                    encoding = self.DEFAULT_ENCODING
                payload_length = self.socket.sendto(bytes(message, encoding), (ip, port))
            response = str(self.socket.recv(self.BUFFER_SIZE), self.DEFAULT_ENCODING)
            return payload_length, response
        except:
            raise Exception("Error sending message")


if "__main__" == __name__:

    # CLI - user convenience
    try:
        cycles = int(sys.argv[1])
        assert 10000 >= cycles > 0
    except (BaseException, ):
        cycles = 10

    try:
        interval = float(sys.argv[2])
        assert 1000.0 >= interval > 0.0
    except (BaseException, ):
        interval = 1.0

    try:
        abcd = ' '.join(sys.argv[3].split('_'))
    except (BaseException, ):
        abcd = [255, 235, 255, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 5, 5, 5, 5, 5, 5, 2, 2, 2, 2, 2, 2, 8, 9, 0, 1,
                2, 3, 4, 5, 6, 7, 8, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # End CLI

    client = Client()

    while cycles > 0:

        cycles -= 1
        # Socket is a byte transfer interface!
        abcd[1] += 1
        length, _response = client.send(bytes(abcd))

        print("Sent: {}".format(abcd))
        print("Received: {}".format(_response))

        time.sleep(interval)
