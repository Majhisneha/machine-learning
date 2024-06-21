# Yaïr Jacob
# original location: pybrain/tools/networking/udpconnection.py
# instrumented function:

        
class MockSocket:
    def __init__(self, recv_behavior=None):
        self.recv_behavior = recv_behavior
        self.recv_called = 0

    def settimeout(self, timeout):
        pass

    def recv(self, buf):
        self.recv_called += 1
        if self.recv_behavior:
            return self.recv_behavior(self.recv_called)
        raise Exception("Simulated recv exception")

    def sendto(self, data, addr):
        pass
    
    def bind(self, addr):
        pass

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
                branch_coverage['branch_5'] = True
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
                branch_coverage['branch_6'] = True
                print("All clients disconnected")
                self.clients = 0
                self.cIP = []
                self.addrList = []
                self.UDPOutSockList = []
                print(("listening on port", self.inPort))

def coverage_report():
    print("\nBranch Coverage Report:")
    for branch, covered in branch_coverage.items():
        print(f"{branch} {'was hit' if covered else 'was not hit'}")
    
    print("Coverage is ", sum(branch_coverage.values()) / len(branch_coverage) * 100, "%")      


branch_coverage = {
    "branch_1": False,
    "branch_2": False,
    "branch_3": False,
    "branch_4": False,
    "branch_5": False,  
    "branch_6": False   
}


server = UDPServer()

# test scenarios
def recv_behavior_scenario_1(call_count):
    if call_count == 1:
        return b'client1'
    raise Exception("Simulated recv exception")

def recv_behavior_scenario_2(call_count):
    if call_count == 1:
        return b'test'
    raise Exception("Simulated recv exception")

def recv_behavior_scenario_3(call_count):
    if call_count == 1:
        return b'newclient'
    raise Exception("Simulated recv exception")


# test1 -> No clients, first recv works, second raises exception
server = UDPServer()
server.UDPInSock = MockSocket(recv_behavior_scenario_1)
coverage_report()

server.listen()
coverage_report()

# test2 -> One client already exists, recv works and matches existing client
server.clients = 1
server.cIP = [b'test']  # fake client
server.UDPInSock = MockSocket(recv_behavior_scenario_2)
server.listen()
coverage_report()

# test3 -> One client already exists, recv works and adds new client
server.clients = 1
server.UDPInSock = MockSocket(recv_behavior_scenario_3)
server.listen()
coverage_report()

# test4 -> No clients, recv raises exception
server = UDPServer()
server.UDPInSock = MockSocket(lambda x: (_ for _ in ()).throw(Exception("Simulated recv exception")))
server.listen()
coverage_report()

# test5 -> One client already exists, recv raises exception
server.clients = 1
server.UDPInSock = MockSocket(lambda x: (_ for _ in ()).throw(Exception("Simulated recv exception")))
server.listen()
coverage_report()

