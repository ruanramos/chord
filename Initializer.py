import select
import socket
import sys
import threading
from multiprocessing import Process
from typing import List

from Node import Node


class Initializer:
    """
    This class handles the initialization of the node ring
    """

    DEFAULT_PORT: int = 9000
    # Empty string indicates the server can receive requests from any network interface
    DEFAULT_HOST: str = ''
    LOGIC_RING_SIZE: int = 16

    # m = 4

    nodes: List[Node] = []  # list of nodes, hash done on id since it's the same IP
    node_processes: List[Process] = []  # 16 processes, one for each node
    client_threads: List[threading.Thread] = []  # Client threads to respond simultaneously

    def __init__(self, step=1):
        self.step = step
        self.entries = [sys.stdin]
        # Start 16 child processes to form the ring
        for node_id in range(0, self.LOGIC_RING_SIZE * step, step):
            # Create a process on port default + node_id
            process = Process(target=self.create_node,
                              args=(node_id % self.LOGIC_RING_SIZE, self.DEFAULT_HOST, self.DEFAULT_PORT + node_id))
            process.start()
            self.node_processes.append(process)
        print(self.node_processes)

        self.create_ring()

        self.accept_connections()

    def accept_connections(self):
        # Waits for the client and listen for connections or stdin commands
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.DEFAULT_HOST, 9500))
            s.listen(5)
            s.setblocking(False)
            self.entries.append(s)

            while True:
                # Listening to connections and commands with select
                print(
                    f"(CONNECTION) Waiting for commands or connections...")
                read, write, error = select.select(self.entries, [], [])
                for read_ready in read:
                    if read_ready == s:  # New connection request
                        s, address = s.accept()
                        print(f"(CONNECTION) Connected to address {address}")

                        # Answer client concurrently
                        thread = threading.Thread(
                            target=self.answer_requests, args=(s, address))
                        self.client_threads.append(thread)  # References for join
                        thread.start()

                    elif read_ready == sys.stdin:
                        # Command line input from server user
                        command = input()

                        if command in ["quit", "q", "exit", "close"]:  # End Initializer
                            for thread in self.client_threads:
                                thread.join()
                                self.client_threads.remove(thread)
                            for p in self.node_processes:
                                p.join()
                                self.node_processes.remove(p)
                            s.close()
                            exit(0)

    def answer_requests(self):
        # TODO  Client has made a request
        # Here the client will ask for a list of nodes, an insert on a specific node
        # or a search from a specific node

        return True

    def create_node(self, node_id, host, port):
        print(f"(INFO) New node is being created")
        node = Node(node_id, host, port, self.step)
        self.nodes.append(node)
        print(f"(INFO) Created node node\n {str(node)}")

    def hash_function(self):
        pass


if __name__ == "__main__":
    i = Initializer(9)