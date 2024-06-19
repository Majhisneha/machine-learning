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
        pass

    def recv(self, buf):
        pass

    def sendto(self, data, addr):
        pass
    def bind(self, addr):
        pass

def coverage_report():
    print("\nBranch Coverage Report:")
    for branch, covered in branch_coverage.items():
        print(f"{branch} {'was hit' if covered else 'was not hit'}")
    
    print("Coverage is ", sum(branch_coverage.values()) / len(branch_coverage) * 100, "%")      


branch_coverage = {
"branch_1": False,
"branch_2": False,
"branch_3": False,
"branch_4": False
}

server = UDPServer()

# simulating different scenarios
coverage_report()

server.listen()
coverage_report()

server.clients = 1
server.listen()
coverage_report()

server.clients = 1
server.cIP = [b'test']  # fake client
server.listen()

coverage_report()