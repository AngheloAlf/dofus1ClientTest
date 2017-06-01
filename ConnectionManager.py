import socket


class ConnectionManager:
    NETBUFFER = 16384

    def __init__(self, showLogs=False):
        # type: (bool) -> None
        self.clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.showLogs = showLogs
        self.connected = False

    def connect(self, ip, port):
        # type: (str, int) -> None
        try:
            self.clientSock.connect((ip, port))
            self.connected = True
            if self.showLogs:
                print "Conexion correcta\n\tIP:" + ip + "\n\tPort:" + str(port)
        except:
            try:
                self.clientSock = ConnectionManager().clientSock
                self.clientSock.connect((ip, port))
                self.connected = True
                if self.showLogs:
                    print "Conexion correcta\n\tIP:" + ip + "\n\tPort:" + str(port)
            except:
                self.connected = False
                print "Ha ocurrido un error al intentar conectar"

    def send(self, packet):
        # type: (str) -> None
        if self.showLogs:
            print "Send >>", packet
        self.clientSock.send(packet + "\n")

    def recv(self, netBuffer=None):
        # type: (int) -> str
        if netBuffer == None:
            recived = self.clientSock.recv(self.NETBUFFER).strip("\x00")
        else:
            recived = self.clientSock.recv(netBuffer).strip("\x00")
        if self.showLogs:
            print "Recv <<", recived
        return recived

    def close(self):
        if self.showLogs:
            print "Cerrando socket"
        self.clientSock.close()
        self.clientSock = None
        self.connected = False
