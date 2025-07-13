import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = []
        self.nicknames = []
        
    def broadcast(self, message):
        """Send message to all connected clients"""
        for client in self.clients:
            try:
                client.send(message)
            except:
                self.remove_client(client)
    
    def remove_client(self, client):
        """Remove client from server"""
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            client.close()
    
    def handle_client(self, client):
        """Handle messages from client"""
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message)
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break
    
    def start_server(self):
        """Start the chat server"""
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.host, self.port))
        server.listen()
        
        print(f'Server is listening on {self.host}:{self.port}')
        
        while True:
            client, address = server.accept()
            print(f'Connected with {str(address)}')
            
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            
            self.nicknames.append(nickname)
            self.clients.append(client)
            
            print(f'Nickname of client is {nickname}')
            self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
            client.send('Connected to server!'.encode('utf-8'))
            
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = ChatServer()
    server.start_server()