from ConnectionManager import ConnectionManager
from CryptManager import CryptManager


class SessionManager(ConnectionManager):
    def __init__(self, showLogs=False):
        # type: (bool) -> None
        ConnectionManager.__init__(self, showLogs)
        self.loggedIn = 0

    def connectRealmServer(self, ip, port):
        # type: (str, int) -> None
        self.connect(ip, port)
        self.realmIP = ip
        self.realmPort = port
        self.xmlData = self.recv()
        self.hashKey = self.recv()[2:]

    def logIn(self, version, username, password):
        # type: (str, str, str) -> bool
        cryptedPass = CryptManager().cryptPassword(self.hashKey, password)
        self.version = version
        self.username = username
        self.password = password
        self.send(version)
        self.send(username)
        self.send(cryptedPass)

        self.loginResponse = self.recv() ##.split(" ") -> [AdApodo, ??, AHEstadoServidores, ??, AQPreguntaSecreta]
        if self.loginResponse == "AlEf":
            if self.showLogs:
                print "Usuario o clave incorrectos"
            self.close()
            return False

        self.send("Af")
        self.recv()  ##Posicion en cola
        self.send("Ax")
        persoSer = self.recv().split("|")

        self.sucript = persoSer[0][3:]
        print "Abono restante:", self.sucript

        self.persoServer = persoSer[1:]
        for i in self.persoServer:
            i = i.split(",")
            print "Servidor " + i[0] + "\n\tPersonajes: " + i[1]

        self.loggedIn = 1
        return True

    def isLoggedIn(self):
        # type: () -> int
        return self.loggedIn

    def getServersList(self):
        # type: () -> list
        return self.persoServer

    def connectGameServer(self, serverToConn):
        # type: (int) -> None
        self.send("AX" + str(serverToConn))
        self.recv()  # EstadoServidor (?)
        gameServerData = self.recv()[3:].split(";")  # AYKip:port;idCuenta
        self.idAccount = gameServerData[1]
        self.gameIP = gameServerData[0].split(":")[0]
        self.gamePort = int(gameServerData[0].split(":")[1])

        self.close()
        self.connect(self.gameIP, self.gamePort)
        self.loggedIn = 2

        self.recv() # HG
        self.send("AT" + self.idAccount)
        self.recv() # ATK0
        self.send("Ak0")
        self.send("AV")
        self.recv() # AV0
        self.send("Ages")
        self.send("Ai099j8kDeZdP8ZJcdW0")
        self.send("AL")
        persosData = self.recv()[3:].split("|") # ALKAbono|CantidadPersonajes|[idPersonaje;nombre;125;100;-1;-1;-1;,,,,;0;1;;;]
        self.sucript = persosData[0]
        self.persos = []
        for i in range(int(persosData[1])):
            self.persos.append(persosData[2+i].split(";"))
        self.send("Af")
        self.recv() # Af1|1|1|1|1

    def getPersos(self):
        return self.persos