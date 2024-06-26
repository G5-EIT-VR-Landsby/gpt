
import socket
import json
import time

def udp_client(server_host='127.0.0.1', server_port=12345):
    """
    A simple UDP client
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send data
        # message = 'Hello, UDP server'
        # message = {
        #     "fagomraade": "1",
        #     "nivaa": "2",
        #     "svarlengde": "1"
        # }
        message = "start 2 2 1"
        print(f"Sending: {message}")
        sock.sendto(message.encode("utf-16"), (server_host, server_port))
        time.sleep(5)

        message = "stop 2 2 1"
        print(f"Sending: {message}")
        sock.sendto(message.encode("utf-16"), (server_host, server_port))

        # # Receive response
        # data, server = sock.recvfrom(1024)
        # print(f"Received: {json.loads(data.decode())}")
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    udp_client()
