
import socket

def udp_client(server_host='127.0.0.1', server_port=12345):
    """
    A simple UDP client
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send data
        message = 'Hello, UDP server'
        print(f"Sending: {message}")
        sock.sendto(message.encode(), (server_host, server_port))

        # Receive response
        data, server = sock.recvfrom(1024)
        print(f"Received: {data.decode()}")
    finally:
        # Close the socket
        sock.close()

if __name__ == "__main__":
    udp_client()
