import socket


class Connection:
    def __init__(self, host="8.8.8.8", port=53, timeout=3):
        self.timeout = timeout
        self.host = host
        self.port = port
        self.check()
    def check(self):
        try:
            socket.setdefaulttimeout(self.timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
            return True
        except OSError:
            return False
