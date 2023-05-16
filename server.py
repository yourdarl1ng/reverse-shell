import socket
import threading 
logs = {}

clients = {}
class ClientHandle:
    def accept(self, socket_a):
        self.socket = socket_a 
        
        self.connection, self.address = self.socket.accept()
        global clients 
        self.ident = 0
        for i in clients:
            self.ident+=1 
        self.ident+=1
        clients[self.ident]=self.connection
        print(self.connection)
        self.data_thread = threading.Thread(target=self.receive_data).start()
    def logs(self, log):
        global logs 
        logs[str(self.address)] = log
    
    def receive_data(self):
       
        while True:
            try:
                self.data = self.connection.recv(2048).decode()
                print(self.data)
                self.logs(self.data)
                if not self.data:
                    global clients
                    clients.pop(self.ident)
                    print(clients)
                    print("removed a client")
                    break
            except:
                
                clients.pop(self.ident)
                print(clients)
                print("removed a client")
                break
    def close(self):
        self.connection.close()
    def send_command(self, command):
        self.connection.send(str(command).encode())
class Server:
    def __init__(self):
        self.port = int 
        self.max_clients = int 
        self.ip = int
        self.connections = []
    def start(self):
        self.read_cfg()
        threading.Thread(target=self.listen).start()
        threading.Thread(target=self.commands).start()
    def commands(self):
        while True:
            self.command = input("command->")
            self.send_all_comms(self.command)
    def send_all_comms(self, command):
        global clients
        for client in clients:
            
            clients[client].send(str(command).encode())
            
           # self.socket.sendall(str(command).encode(), address)
    def read_cfg(self):
        try:
            with open("server.cfg", "r") as config:
                self.lines = config.read()
                self.port = int(self.lines.split("\n")[0].split("=")[1])
                self.max_clients = int(self.lines.split("\n")[1].split("=")[1])
                self.ip = self.lines.split("\n")[2].split("=")[1]
                config.close()
            print("[LOGS]: Config loaded")
        except Exception as e:
            print(e)
            with open("server.cfg", "w+") as config:
                self.localip = socket.gethostbyname(socket.gethostname())
                config.write(f"port=4465\nmax clients=500\nip={self.localip}\n")
                self.port = 4465
                self.max_clients = 500
                self.ip = self.localip
                config.close()
            print("[LOGS]: config made")
    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, int(self.port)))
        self.socket.listen(self.max_clients)
        while True:
            ClientHandle().accept(self.socket)
            
            
            print("Accepted a new client connection")
            #print(clients)
            self.save_logs()
    def save_logs(self):
        with open("logs.txt", "r") as log:
            log_data = log.read()
            log.close() 
        with open("logs.txt", "w") as log:
            global logs
            log.write(log_data + f"\n{logs}")
            logs.clear()
            log.close()
Server().start()
