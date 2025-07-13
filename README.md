# Socket Programming Chat Application

A simple multi-client chat application built with Python socket programming.

## Features

- **Multi-client support**: Multiple users can join the chat simultaneously
- **Real-time messaging**: Messages are broadcast to all connected clients instantly
- **User nicknames**: Each client chooses a unique nickname
- **Connection notifications**: Users are notified when someone joins/leaves

## How It Works

### Server (`server.py`)
- Creates a socket server that listens on localhost:12345
- Uses threading to handle multiple clients concurrently
- Maintains lists of connected clients and their nicknames
- Broadcasts messages from one client to all other clients
- Handles client disconnections gracefully

### Client (`client.py`)
- Connects to the server using socket
- Uses separate threads for sending and receiving messages
- Prompts user for nickname on startup
- Displays all chat messages in real-time

## Usage

### 1. Start the Server
```bash
python server.py
```
The server will start listening on localhost:12345

### 2. Connect Clients
Open new terminal windows and run:
```bash
python client.py
```
Each client will prompt for a nickname, then you can start chatting!

### 3. Chat
- Type messages and press Enter to send
- Messages appear as: `nickname: message`
- Join/leave notifications are automatically broadcast

## Technical Details

### Socket Programming Concepts Used:
- **TCP Sockets**: Reliable connection-oriented communication
- **Threading**: Handle multiple clients simultaneously
- **Broadcasting**: Send messages to all connected clients
- **Error Handling**: Graceful client disconnection management

### Key Methods:
- `socket.socket()`: Create socket object
- `bind()`: Bind socket to address
- `listen()`: Listen for connections
- `accept()`: Accept client connections
- `send()/recv()`: Send/receive data
- `threading.Thread()`: Create separate threads

## Example Session

```
Server Output:
Server is listening on localhost:12345
Connected with ('127.0.0.1', 54321)
Nickname of client is Alice

Client Output:
Choose a nickname: Alice
Connected to server!
Alice joined the chat!
Alice: Hello everyone!
Bob joined the chat!
Bob: Hi Alice!
```

## Stopping the Application

- **Server**: Press Ctrl+C to stop the server
- **Client**: Press Ctrl+C to disconnect from chat