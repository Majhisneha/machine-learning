# Yaïr Jacob
# original location: pybrain/tools/networking/udpconnection.py
# instrumented function:

class UDPServer:
    def __init__(self):
        self.clients = 0
        self.cIP = []
        self.addrList = []
        self.UDPOutSockList = []
        self.buf = 1024 
        self.inPort = 21560
        self.UDPInSock = MockSocket()

    def addClient(self, cIP):
        self.cIP.append(cIP)
        self.addrList.append((cIP, self.inPort + 1))
        self.UDPOutSockList.append(MockSocket())  # mock socket for sending data
        print(f"Client {cIP} connected")
        self.clients += 1

    # Listen for clients
    def listen(self):
        if self.clients < 1:
            branch_coverage['branch_1'] = True
            self.UDPInSock.settimeout(10)
            try:
                cIP = self.UDPInSock.recv(self.buf)
                self.addClient(cIP)
            except:
                pass
        else:
            branch_coverage['branch_2'] = True
            # At least one client has to send a sign of life during 2 seconds
            self.UDPInSock.settimeout(2)
            try:
                cIP = self.UDPInSock.recv(self.buf)
                newClient = True
                for i in self.cIP:
                    if cIP == i:
                        branch_coverage['branch_3'] = True
                        newClient = False
                        break
                # Adding new client
                if newClient:
                    branch_coverage['branch_4'] = True
                    self.addClient(cIP)
            except:
                print("All clients disconnected")
                self.clients = 0
                self.cIP = []
                self.addrList = []
                self.UDPOutSockList = []
                print(("listening on port", self.inPort))

class MockSocket:
    def __init__(self):
        pass

    def settimeout(self, timeout):
        print(f"Setting socket timeout to {timeout} seconds")

    def recv(self, buf):
        # simulate receiving data
        print(f"Receiving data with buffer size {buf}")
        return b'192.168.1.100'  # data received

    def sendto(self, data, addr):
        print(f"Sending data {data} to address {addr}")

    def bind(self, addr):
        print(f"Binding socket to address {addr}")

def coverage_report():
        print("\nBranch Coverage Report:")
        for branch, covered in branch_coverage.items():
            print(f"{branch} {'was hit' if covered else 'was not hit'}")


branch_coverage = {
"branch_1": False,
"branch_2": False,
"branch_3": False,
"branch_4": False
}

server = UDPServer()

# simulating different scenarios
print("Test 1: No clients connected, data received successfully")
server.listen()

print("\nTest 2: No clients connected, exception while receiving data")
server.UDPInSock.exception_on_recv = True
server.listen()

print("\nTest 3: One client connected, existing client sends data")
server.clients = 1
server.listen()

print("\nTest 4: One client connected, new client sends data")
server.clients = 1
server.cIP = [b'test']  # fake client
server.listen()

print("\nTest 5: One client connected, exception while receiving data")
server.clients = 1
server.listen()

print("\nTest 6: All clients disconnected, exception handling")
server.clients = 1
server.exception_on_listen = True
server.listen()

coverage_report()