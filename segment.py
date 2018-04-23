class segment:
	
	int numSegments = 0
	
	def __init__(self, numSegments, array, sortBy):
		self.numSegments = numSegments
		array = np.copy(array)
		array = array.reshape(len(array)/8, 8)
		
		array = np.sort(array, 5+sortBy)