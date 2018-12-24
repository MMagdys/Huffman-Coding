class HuffmanNode(object):

	def __init__(self,char, freq, left=None, right=None):

		self.char = char
		self.freq = freq
		self.left = left
		self.right = right


	def __lt__(self, other):

		return self.freq < other.freq


	def __str__(self):

		return "(" + self.char + " : " + str(self.freq) + ")"


	def __repr__(self):

		return self.__str__()



class TreeNode(object):

	def __init__(self, char="", left=None, right=None):

		self.char = char
		self.left = left
		self.right = right



	def __str__(self):

		return  self.char 


	def __repr__(self):

		return self.__str__()