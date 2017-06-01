import Tkinter
import ttk
from functools import partial
import tkMessageBox
from SessionManager import SessionManager

SESION_INICIADA = False


def milisegundosAString(milis):
    return str(int(milis)/1000)+" s"


def obtenerUsuario(entries, lista, clientSession, listaServidores):
    # type: (list, list, SessionManager, list) -> list
    if clientSession.isLoggedIn():
        tkMessageBox.showerror("Error", "La sesion ya esta iniciada")
        return lista

    lista[0] = entries[0].get()
    lista[1] = int(entries[1].get())
    lista[2] = entries[2].get()
    lista[3] = entries[3].get()
    lista[4] = entries[4].get()
    #programa.destroy()
    print lista

    clientSession.connectRealmServer(lista[0], lista[1])
    if clientSession.logIn(lista[2], lista[3], lista[4]):
        serversList = clientSession.getServersList()
        for serv in range(len(serversList)):
            listaServidores[serv]['state'] = "normal"
            listaServidores[serv]["text"] = "Conectar | " + serversList[serv].split(",")[1]

    return lista

def conectarAServidor(clientSession, selectedServer, charactersList):
    # type: (SessionManager, int, list) -> list
    clientSession.connectGameServer(selectedServer)
    persos = clientSession.getPersos()
    for i in range(len(persos)):
        charactersList[i]['state'] = "normal"
        charactersList[i]["text"] = persos[i][0] + " | " + persos[i][1]

    return

def mandarComando(entry, clientSocket):
    if entry.get() == "":
        return
    clientSocket.send(entry.get())

def main():
    listaDatos = ["", "", "", "", ""]
    inputsList = []
    listaServidores = []
    listaPersonajes = []
    clientSession = SessionManager(True)

    programa = Tkinter.Tk()
    programa.minsize(210*4,200)

    labelframe = ttk.LabelFrame(programa, text="Inicio de sesion")
    labelframe.pack(fill="both", expand="yes", side=Tkinter.LEFT)

    L1 = ttk.Label(labelframe, text="IP: ")
    E1 = ttk.Entry(labelframe)
    E1.insert(0, "127.0.0.1")
    L1.place(x=0,y=0)
    E1.place(x=75, y=0)

    L2 = ttk.Label(labelframe, text="Port: ")
    E2 = ttk.Entry(labelframe)
    E2.insert(0, "444")
    L2.place(x=0,y=25)
    E2.place(x=75, y=25)

    L3 = ttk.Label(labelframe, text="Version: ")
    E3 = ttk.Entry(labelframe)
    E3.insert(0, "1.29.1")
    L3.place(x=0,y=50)
    E3.place(x=75, y=50)

    L4 = ttk.Label(labelframe, text="Usuario: ")
    E4 = ttk.Entry(labelframe)
    E4.insert(0, "")
    L4.place(x=0,y=75)
    E4.place(x=75, y=75)

    L5 = ttk.Label(labelframe, text="Clave: ")
    E5 = ttk.Entry(labelframe)
    E5.insert(0, "")
    L5.place(x=0,y=100)
    E5.place(x=75, y=100)

    inputsList.append(E1)
    inputsList.append(E2)
    inputsList.append(E3)
    inputsList.append(E4)
    inputsList.append(E5)

    B1 = ttk.Button(labelframe, text ="Logear", command = partial(obtenerUsuario, inputsList, listaDatos, clientSession, listaServidores))
    B1.place(x=100, y=150)


    labelframeServidor = ttk.LabelFrame(programa, text="Seleccion de servidor")
    labelframeServidor.pack(fill="both", expand="yes", side=Tkinter.LEFT)

    for i in range(5):
        servidorL = ttk.Label(labelframeServidor, text="Servidor " + str(i + 1) + ": ")
        servidorL.place(x=25, y=25*i)
        servidorB = ttk.Button(labelframeServidor, text="Conectar", state=Tkinter.DISABLED, command=partial(conectarAServidor, clientSession, i+1, listaPersonajes)) # command=partial(conecetarServidor, i, clientSocket))
        servidorB.place(x=100, y=25*i)
        listaServidores.append(servidorB)



    labelframePersonaje = ttk.LabelFrame(programa, text="Seleccion de personaje")
    labelframePersonaje.pack(fill="both", expand="yes", side=Tkinter.LEFT)

    for i in range(5):
        servidorL = ttk.Label(labelframePersonaje, text="Personaje " + str(i + 1) + ": ")
        servidorL.place(x=25, y=25*i)
        servidorB = ttk.Button(labelframePersonaje, text="Seleccionar", state=Tkinter.DISABLED) # , command=partial(clientSession.connectGameServer, i+1)) # command=partial(conecetarServidor, i, clientSocket))
        servidorB.place(x=100, y=25*i)
        listaPersonajes.append(servidorB)



    labelframeComandos = ttk.LabelFrame(programa, text="Comandos")
    labelframeComandos.pack(fill="both", expand="yes", side=Tkinter.LEFT)

    L6 = ttk.Label(labelframeComandos, text="Comando: ")
    E6 = ttk.Entry(labelframeComandos)
    L6.place(x=0,y=0)
    E6.place(x=75, y=0)

    B2 = ttk.Button(labelframeComandos, text ="Mandar comando", command = partial(mandarComando, E6, clientSession))
    B2.place(x=10, y=50)
    recvButton = ttk.Button(labelframeComandos, text ="Recv", command = clientSession.recv)
    recvButton.place(x=125, y=50)




    # B2.place(x=100, y=250)



    programa.mainloop()

    clientSession.close()

    print listaDatos

if __name__ == "__main__":
    main()