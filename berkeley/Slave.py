from time import time, gmtime, strftime
import zmq
import random
import zmq
from datetime import datetime

class Slave():
    """
    Clase Slave
    """
    def __init__(self, port = 5555):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:{}".format(port))
        self.ajuste = 0
        self.desvio_aleatorio = self.get_desvio_aleatorio()
        self.tiempo_actual = time() + self.ajuste + self.desvio_aleatorio
    
    def get_time(self):
        self.tiempo_actual = time() + self.ajuste + self.desvio_aleatorio
        return self.tiempo_actual
    
    def get_human_time(self):
        return strftime("%H:%M:%S",gmtime(self.get_time()))

    def set_ajuste(self, ajuste:float):
        self.ajuste = float(ajuste)
    
    def get_desvio_aleatorio(self):
        return random.random() * random.randint(-100, 100)
    
    def escuchar(self):
        while True:
            try:
                message = self.socket.recv()
                if message.decode('utf-8') == "dame_tiempo":
                    self.socket.send(str(self.get_time()).encode('utf-8'))
                else:
                    self.set_ajuste(message.decode('utf-8'))
                    self.socket.send(str(self.get_time()).encode('utf-8'))
            except:
                pass
