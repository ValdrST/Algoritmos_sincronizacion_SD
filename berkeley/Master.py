from time import time, gmtime, strftime
import zmq

class Master():
    """
    Clase Master
    """
    def __init__(self):
        self.suma_diferencias = 0
        self.slaves = []
        self.tiempos = []
        self.tiempo_sincronizado = time()
        self.diferencia_media = 0

    def registrar_slave(self, port):
        self.slaves.append(port)
    
    def get_time(self):
        return self.tiempo_sincronizado

    def get_human_time(self):
        return strftime("%H:%M:%S",gmtime(self.get_time()))
    
    def obtener_tiempos(self):
        self.tiempos = []
        for slave in self.slaves:
            self.tiempos.append(self.obtener_tiempo_slave(slave))
    
    def obtener_tiempo_slave(self, slave):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:{}".format(slave))
        socket.send("dame_tiempo".encode('utf-8'))
        return float(socket.recv().decode('utf-8'))
    
    def enviar_ajuste(self):
        cont = 0
        for slave in self.slaves:
            dif =  self.tiempo_sincronizado - self.tiempos[cont] 
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:{}".format(slave))
            socket.send(str(dif).encode('utf-8'))
            cont += 1

    def work(self):
        self.obtener_tiempos()
        self.sumar_diferencias()
        self.calcular_diferencia_media()
        self.tiempo_sincronizado = time() + self.diferencia_media
        self.enviar_ajuste()
        
    def calcular_diferencia_media(self):
        self.diferencia_media = self.suma_diferencias / (len(self.slaves) + 1)

    def sumar_diferencias(self):
        self.suma_diferencias = 0
        for tiempo in self.tiempos:
            diferencia = tiempo - time()
            self.suma_diferencias += diferencia
