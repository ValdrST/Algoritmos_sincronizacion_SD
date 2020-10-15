from threading import Thread
from Slave import Slave
from Master import Master
from time import sleep


if __name__ == '__main__':
    master = Master()
    print("Master tiempo {}".format(master.get_human_time()))
    slave1 = Slave(10000)
    slave2 = Slave(10001)
    slave3 = Slave(10002)
    slave4 = Slave(10003)
    master.registrar_slave(10000)
    master.registrar_slave(10001)
    master.registrar_slave(10002)
    master.registrar_slave(10003)
    print("slave 1 tiempo {}".format(slave1.get_human_time()))
    t1 = Thread(target=slave1.escuchar)
    t1.start()
    print("slave 2 tiempo {}".format(slave2.get_human_time()))
    t2 = Thread(target=slave2.escuchar)
    t2.start()
    print("slave 3 tiempo {}".format(slave3.get_human_time()))
    t3 = Thread(target=slave3.escuchar)
    t3.start()
    print("slave 4 tiempo {}".format(slave4.get_human_time()))
    t4 = Thread(target=slave4.escuchar)
    t4.start()
    master.work()

    print(master.diferencia_media)
    print("Master ajustado tiempo {}".format(master.get_human_time()))
    print("slave 1 ajustado tiempo {}".format(slave1.get_human_time()))
    print("slave 2 ajustado tiempo {}".format(slave2.get_human_time()))
    print("slave 3 ajustado tiempo {}".format(slave3.get_human_time()))
    print("slave 4 ajustado tiempo {}".format(slave4.get_human_time()))

    