import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog

class ChatClientGUI:
    def __init__(self):
        self.host = 'localhost'
        self.port = 12345
        self.nickname = ""
        self.client = None
        self.connected = False
        
        self.setup_gui()
        
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Chat Client")
        self.root.geometry("500x600")
        
        # Connection frame
        conn_frame = tk.Frame(self.root)
        conn_frame.pack(pady=10)
        
        self.connect_btn = tk.Button(conn_frame, text="Connect", command=self.connect_to_server, bg="green", fg="white")
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_btn = tk.Button(conn_frame, text="Disconnect", command=self.disconnect, bg="red", fg="white", state="disabled")
        self.disconnect_btn.pack(side=tk.LEFT, padx=5)
        
        # Status
        self.status_label = tk.Label(self.root, text="Status: Disconnected", font=("Arial", 10))
        self.status_label.pack()
        
        # Chat display
        tk.Label(self.root, text="Chat Messages:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10,0))
        self.chat_display = scrolledtext.ScrolledText(self.root, height=20, state="disabled", wrap=tk.WORD)
        self.chat_display.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Message input
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill="x", padx=20, pady=5)
        
        self.message_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.message_entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_btn = tk.Button(input_frame, text="Send", command=self.send_message, bg="blue", fg="white", state="disabled")
        self.send_btn.pack(side=tk.RIGHT, padx=(5,0))
        
    def display_message(self, message):
        self.chat_display.config(state="normal")
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state="disabled")
        
    def connect_to_server(self):
        # Get nickname
        self.nickname = simpledialog.askstring("Nickname", "Enter your nickname:")
        if not self.nickname:
            return
            
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, self.port))
            self.connected = True
            
            # Update UI
            self.status_label.config(text=f"Status: Connected as {self.nickname}")
            self.connect_btn.config(state="disabled")
            self.disconnect_btn.config(state="normal")
            self.send_btn.config(state="normal")
            self.message_entry.config(state="normal")
            
            # Start receiving messages
            threading.Thread(target=self.receive_messages, daemon=True).start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server: {e}")
            
    def receive_messages(self):
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    self.display_message(message)
            except:
                if self.connected:
                    self.display_message("Connection lost!")
                    self.disconnect()
                break
                
    def send_message(self, event=None):
        if not self.connected:
            return
            
        message = self.message_entry.get().strip()
        if message:
            try:
                full_message = f'{self.nickname}: {message}'
                self.client.send(full_message.encode('utf-8'))
                self.message_entry.delete(0, tk.END)
            except:
                self.display_message("Failed to send message!")
                
    def disconnect(self):
        self.connected = False
        if self.client:
            self.client.close()
            
        # Update UI
        self.status_label.config(text="Status: Disconnected")
        self.connect_btn.config(state="normal")
        self.disconnect_btn.config(state="disabled")
        self.send_btn.config(state="disabled")
        self.message_entry.config(state="disabled")
        self.display_message("Disconnected from server")
        
    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
        
    def on_closing(self):
        if self.connected:
            self.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    client_gui = ChatClientGUI()
    client_gui.run()