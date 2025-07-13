import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.nickname = input("Choose a nickname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def receive_messages(self):
        """Receive messages from server"""
        while True:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("An error occurred!")
                self.client.close()
                break
    
    def send_messages(self):
        """Send messages to server"""
        while True:
            message = f'{self.nickname}: {input("")}'
            self.client.send(message.encode('utf-8'))
    
    def start_client(self):
        """Connect to server and start messaging"""
        try:
            self.client.connect((self.host, self.port))
            
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            send_thread = threading.Thread(target=self.send_messages)
            send_thread.daemon = True
            send_thread.start()
            
            send_thread.join()
            
        except Exception as e:
            print(f"Could not connect to server: {e}")

if __name__ == "__main__":
    client = ChatClient()
    client.start_client()