
from http.client import responses
import socket
import json

class Server:

    def __init__(self, host="localhost", port=12345) -> None:
        self.host = host
        self.port = port
        self.global_context = None
        self.context_list = None
        self.recoding_flag = False

    def decode_message(self, raw_message):
        string_msg = raw_message.decode("utf-16")
        vars = string_msg.split(" ")

        # Toggle recoding flag
        self.recoding_flag = True if vars[0] == "start" else False
        print(f"[udp_server] recoding_flag {self.recoding_flag}")

        # Remove first value
        self.context_list = vars[1:]
        print(f"[udp_server] context_list {self.context_list}")
        
        return vars

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

                decoded_msg = self.decode_message(data) # to list

                # decoded_msg = json.loads(data)
                print(f"[UDP server]: Received message: {decoded_msg} from {addr}")
                # self.global_context = decoded_msg

                # response = "Message received"
                # sock.sendto(json.dumps(response), addr)
        except KeyboardInterrupt:
            print("\nServer is shutting down.")
        finally:
            # Close the socket to clean up
            sock.close()

if __name__ == "__main__":
    
    t = Server()
    t.start()
