import socket
import sys
from typing import List, Any, Dict


class Node:
    socket: socket.socket
    entries: List[Any] = [sys.stdin]
    connections: List[Any] = []
    finger_table: Dict[Any, Any] = {}

    def __init__(self, node_id: int, host: str, port: int, step: int):
        self.id = node_id
        self.port = port
        self.host = host
        self.step = step

        # # m = number of bits in the hash key = 4
        # # the ith entry of node n will contain successor( (n + 2^(i-1) ) mod 2^m)

    def create_socket(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port + i))
            s.listen(5)
            s.setblocking(False)
            self.entries.append(s)
            self.socket = s

            # while True:
            #     # Listening to connections and commands with select
            #     print(f"(CONNECTION) Node is waiting for commands or connections...")
            #     read, write, error = select.select(self.entries, [], [])
            #     for read_ready in read:
            #         if read_ready == s:  # New connection request
            #             client_socket, address = s.accept()
            #             self.connections.append(client_socket)
            #             print(f"(CONNECTION) Connected to node {address}")
            #
            #             # TODO Answer the request from the "Server" or initializer
            #             client_thread = threading.Thread()
            #
            #         elif read_ready == sys.stdin:
            #             # Command line input from server user
            #             command = input()
            #
            #             if command in ["quit", "q", "exit", "close"]:  # End server
            #                 for process in self.node_processes:
            #                     process.join()
            #                     self.node_processes.remove(process)
            #                 s.close()
            #                 exit(0)

    def __str__(self):
        return f"Node id: {self.id}\nNode Port: {self.port}\nNode Host: {self.host}"

    # def insert_pair(self, key, value):
    #
    # def find_key(self):
    #
    # def generate_hash(self):
    #
    # def set_finger_table(self):
    #     # For 16 nodes, 4 entries