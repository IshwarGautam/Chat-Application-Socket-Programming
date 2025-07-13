# Socket Programming Chat Application

A simple multi-client chat application built with Python socket programming, available in both terminal and GUI versions.

## Features

- **Multi-client support**: Multiple users can join the chat simultaneously
- **Real-time messaging**: Messages are broadcast to all connected clients instantly
- **User nicknames**: Each client chooses a unique nickname
- **Connection notifications**: Users are notified when someone joins/leaves
- **GUI Interface**: Easy-to-use graphical interface with server monitoring
- **Active Client Tracking**: Server GUI shows all connected clients in real-time

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

### Terminal Version

#### 1. Start the Server
```bash
python server.py
```

#### 2. Connect Clients
```bash
python client.py
```

### GUI Version (Recommended)

#### 1. Start the Server GUI
```bash
python server_gui.py
```
- Click "Start Server" button
- Monitor active clients and server logs in real-time

#### 2. Connect Client GUIs
```bash
python client_gui.py
```
- Click "Connect" and enter your nickname
- Start chatting in the message box
- Press Enter or click "Send" to send messages

### Features:
- **Server GUI**: Shows active clients list and message logs
- **Client GUI**: Clean chat interface with connect/disconnect buttons
- **Real-time Updates**: Instant message delivery and client status updates

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

### Terminal Version:
- **Server**: Press Ctrl+C to stop the server
- **Client**: Press Ctrl+C to disconnect from chat

### GUI Version:
- **Server**: Click "Stop Server" button or close window
- **Client**: Click "Disconnect" button or close window