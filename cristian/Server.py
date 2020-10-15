from time import time, gmtime, strftime
import zmq
from timeit import timeit

class Server():
    """
    Clase Server
    """
    def __init__(self):
        self.slaves = []
        self.tiempos = []
        self.tiempos_round = [] 

    def registrar_slave(self, port):
        self.slaves.append(port)
    
    def get_time(self):
        return time() # time() es el equivalente a obtener el tiempo del UTC

    def get_human_time(self):
        return strftime("%H:%M:%S",gmtime(self.get_time()))
    
    def obtener_tiempos(self):
        self.tiempos = []
        for slave in self.slaves:
            tiempo_inicio = time()
            self.tiempos.append(self.obtener_tiempo_slave(slave))
            tiempo_fin = time()
            self.tiempos_round.append(tiempo_fin-tiempo_inicio)
    
    def obtener_tiempo_slave(self, slave):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:{}".format(slave))
        socket.send("dame_tiempo".encode('utf-8'))
        return float(socket.recv().decode('utf-8'))
    
    def enviar_ajuste(self):
        cont = 0
        for slave in self.slaves:
            dif = time() + (self.tiempos_round[cont]/2)
            context = zmq.Context()
            socket = context.socket(zmq.REQ)
            socket.connect("tcp://localhost:{}".format(slave))
            socket.send(str(dif).encode('utf-8'))
            cont += 1

    def work(self):
        self.obtener_tiempos()
        self.enviar_ajuste()
        
