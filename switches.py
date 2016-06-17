class Switch():
	def __init__(self, switchId, switchState):
		self.sid = switchId
		self.state = switchState

class MySwitches():
	def __init__(self):
		self.ID1 = Switch('11111', False)
		self.ID2 = Switch('22222', False)
		self.ID3 = Switch('33333', False)
		