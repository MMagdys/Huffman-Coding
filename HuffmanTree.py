from HuffmanNode import HuffmanNode
import heapq
from collections import Counter


class HuffmanTree(object):
	
	def __init__(self, root=None):

		self.root = root
		self.heap = []
		self.CODES = {}
		self.enc_tree = bytearray()



	def char_frequency(self, txt):

		'''
		txt(str) -> char frequency (dict)

		This Function calculates the number of times a character appears in Text
		and return min heap of char according to their frequency

		'''

		char_freq =  Counter(txt)
		self.heap = [HuffmanNode(char, freq) for char, freq in char_freq.items()]
		heapq.heapify(self.heap)

		return self.heap



	def tree_build(self):

		'''
		Build tree from Min heap, which is 
		sorted due to character frequency in text
		'''

		while (len(self.heap) > 1):

			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			freq = int(node1.freq) + int(node2.freq)

			heapq.heappush(self.heap, HuffmanNode("IN", freq, node1, node2))

		self.root = heapq.heappop(self.heap)



	def generate_codes(self, root , code = ""):

		'''
		root(HuffmanNode), code(str) -> UPDATE CODES(dict)

		Create Huffman Code for each character Recursively
		By traversing over the nodes starting from the Root
		adding "0" bit for each left step
		adding "1" bit fro each right step
		'''

		if root.left is None:
			if code == "":
				self.CODES[root.char] = 0 
				return
			self.CODES[root.char] = code
			return

		left = root.left
		right = root.right
		
		self.generate_codes(left, code+"0")
		self.generate_codes(right, code+"1")



	def encoded_tree(self, root=None):

		if root is None:
			root = self.root


		if root.left is None:
			self.enc_tree.append(ord("0"))
			self.enc_tree.append(root.char)

		else:

			left = root.left
			right = root.right
			
			self.enc_tree.append(ord("1"))
			self.encoded_tree(left)
			self.encoded_tree(right)

		return self.enc_tree



	def huffman_coding(self, txt):

		self.char_frequency(txt)
		self.tree_build()
		self.generate_codes(self.root)
		self.encoded_tree()

		return self.CODES, self.enc_tree

