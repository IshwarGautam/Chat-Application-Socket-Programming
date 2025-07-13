import socket
import threading
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext

class ChatServerGUI:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.clients = []
        self.nicknames = []
        self.server_running = False
        
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Chat Server - Control Panel")
        self.root.geometry("600x500")
        
        # Server controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.start_btn = tk.Button(control_frame, text="Start Server", command=self.start_server, bg="green", fg="white")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="Stop Server", command=self.stop_server, bg="red", fg="white", state="disabled")
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Server status
        self.status_label = tk.Label(self.root, text="Server Status: Stopped", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Active clients list
        tk.Label(self.root, text="Active Clients:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20)
        self.clients_listbox = tk.Listbox(self.root, height=6)
        self.clients_listbox.pack(fill="x", padx=20, pady=5)
        
        # Server logs
        tk.Label(self.root, text="Server Logs:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20)
        self.log_text = scrolledtext.ScrolledText(self.root, height=15, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=20, pady=5)
        
    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
    def update_clients_list(self):
        self.clients_listbox.delete(0, tk.END)
        for nickname in self.nicknames:
            self.clients_listbox.insert(tk.END, nickname)
            
    def broadcast(self, message):
        for client in self.clients[:]:
            try:
                client.send(message)
            except:
                self.remove_client(client)
                
    def remove_client(self, client):
        if client in self.clients:
            index = self.clients.index(client)
            self.clients.remove(client)
            nickname = self.nicknames[index]
            self.nicknames.remove(nickname)
            self.broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            self.log_message(f"Client {nickname} disconnected")
            self.update_clients_list()
            client.close()
            
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message)
                    decoded_msg = message.decode('utf-8')
                    self.log_message(f"Message: {decoded_msg}")
                else:
                    self.remove_client(client)
                    break
            except:
                self.remove_client(client)
                break
                
    def start_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.host, self.port))
            self.server.listen()
            self.server_running = True
            
            self.status_label.config(text=f"Server Status: Running on {self.host}:{self.port}")
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            self.log_message(f"Server started on {self.host}:{self.port}")
            
            threading.Thread(target=self.accept_clients, daemon=True).start()
            
        except Exception as e:
            self.log_message(f"Error starting server: {e}")
            
    def accept_clients(self):
        while self.server_running:
            try:
                client, address = self.server.accept()
                self.log_message(f"Connection from {address}")
                
                client.send('NICK'.encode('utf-8'))
                nickname = client.recv(1024).decode('utf-8')
                
                self.nicknames.append(nickname)
                self.clients.append(client)
                
                self.log_message(f"Client nickname: {nickname}")
                self.update_clients_list()
                self.broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
                client.send('Connected to server!'.encode('utf-8'))
                
                threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()
                
            except:
                break
                
    def stop_server(self):
        self.server_running = False
        if hasattr(self, 'server'):
            self.server.close()
        self.status_label.config(text="Server Status: Stopped")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.log_message("Server stopped")
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        if self.server_running:
            self.stop_server()
        self.root.destroy()

if __name__ == "__main__":
    server_gui = ChatServerGUI()
    server_gui.run()