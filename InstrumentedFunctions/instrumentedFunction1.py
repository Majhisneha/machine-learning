# Yaïr Jacob
# original location: (pybrain/rl/environments/twoplayergames/capturegameplayers/clientwrapper.py)
# instrumented function:

branch_coverage = {
    "branch_1": False,
    "branch_2": False,
    "branch_3": False,
    "branch_4": False,
    "branch_5": False,
    "branch_6": False,
}

class CaptureGame:
    BLACK = 'BLACK'
    WHITE = 'WHITE'

class Game:
    def __init__(self, size):
        self.size = size
        self.b = {}  # empty dictionary for the board

    def _iterPos(self): # iterator board pos
        for i in range(self.size * self.size): 
            yield i

class MockObject:
    def __init__(self, color=CaptureGame.BLACK, board_data=None):
        self.color = color
        self.game = Game(size=4)
        if board_data:
            self.game.b = board_data

# data for Branch 1 (obj.color == CaptureGame.BLACK)
branch_1_data = {
    0: CaptureGame.BLACK,   
    1: CaptureGame.WHITE,
    2: CaptureGame.BLACK,
    3: CaptureGame.WHITE,
}

# data for Branch 2 (else condition)
branch_2_data = {
    0: CaptureGame.WHITE,    
    1: CaptureGame.BLACK,
    2: CaptureGame.WHITE,
    3: CaptureGame.BLACK,
}

# scenario ensures the first position of each row is hit
branch_3_data = {
    0: CaptureGame.BLACK,
    4: CaptureGame.WHITE,
    8: CaptureGame.BLACK,
    12: CaptureGame.WHITE,
}

# data for Branch 4 (obj.game.b.get(p, None) == CaptureGame.BLACK)
branch_4_data = {
    0: CaptureGame.BLACK,
    1: CaptureGame.WHITE,
    2: CaptureGame.BLACK,
    3: CaptureGame.BLACK,
}


# data for Branch 5 (elif obj.game.b.get(p, None) == CaptureGame.WHITE)
branch_5_data = {
    0: CaptureGame.WHITE,
    1: CaptureGame.BLACK,
    2: CaptureGame.WHITE,
    3: CaptureGame.WHITE,
}

# data for Branch 6 (else condition)
branch_6_data = {
    0: 'random',
    1: 'random2',
    2: 'random3',
    3: 'random4',
}

mock_objects = [
    MockObject(color=CaptureGame.BLACK, board_data=branch_1_data),
    MockObject(color=CaptureGame.WHITE, board_data=branch_2_data),
    MockObject(color=CaptureGame.BLACK, board_data=branch_3_data),
    MockObject(color=CaptureGame.BLACK, board_data=branch_4_data),
    MockObject(color=CaptureGame.WHITE, board_data=branch_5_data),
    MockObject(color=CaptureGame.WHITE, board_data=branch_6_data),
]


# function to test
def getAction(obj):
    # build a java string
    if obj.color == CaptureGame.BLACK:
        branch_coverage['branch_1'] = True
        js = '1-'
    else:
        branch_coverage['branch_2'] = True
        js = '2-'
    for i, p in enumerate(obj.game._iterPos()):
        if i % obj.game.size == 0:
            branch_coverage['branch_3'] = True
            js += '-'
        if obj.game.b.get(p, None) == CaptureGame.BLACK:
            branch_coverage['branch_4'] = True
            js += '1'
        elif obj.game.b.get(p, None) == CaptureGame.WHITE:
            branch_coverage['branch_5'] = True
            js += '2'
        else:
            branch_coverage['branch_6'] = True
            js += '0'

    return js 

def print_coverage():
    for branch, hit in branch_coverage.items():
        print(f"{branch} was {'hit' if hit else 'not hit'}")


# run tests
for mock_obj in mock_objects:
    result = getAction(mock_obj)

print("Coverage:")
print_coverage()