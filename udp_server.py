
from http.client import responses
import socket


class Server:

    def __init__(self, host="localhost", port=12345) -> None:
        self.host = host
        self.port = port

    def start(self):
        # Create a socket object
        # socket.AF_INET indicates that we'll use IPv4 addresses
        # socket.SOCK_DGRAM indicates that this will be a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to an address and port
        # The address is a tuple consisting of IP address and port number
        sock.bind((self.host, self.port))

        print(f"[UDP server]: Up and listening at {self.host}:{self.port}")

        try:
            while True:  # Keep the server running
                # Receive message from client
                data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
                print(f"[UDP server]: Received message: {data.decode()} from {addr}")

                # Optionally, send a response back to the client
                response = "Message received"
                sock.sendto(response.encode(), addr)
        except KeyboardInterrupt:
            print("\nServer is shutting down.")
        finally:
            # Close the socket to clean up
            sock.close()

if __name__ == "__main__":
    
    t = Server()
    t.start()
