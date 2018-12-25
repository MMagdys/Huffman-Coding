from HuffmanNode import TreeNode


class HuffmanDecoder(object):

	def __init__(self, root=None):

		self.root = root



	def build_tree(self, tree_bytes):

		'''
		tree_byte(bytesarray) -> root(TreeNode)

		------------
		This function Rebuild Huffman Tree from encoded 
		tree bytes.

		Building Algorthim
		------------------
		1 : Internal Node 
		0 : Leaf Node
		'''

		ch = tree_bytes.pop(0)

		if ch is None:
			return

		if ch == 48:
 
 			root = TreeNode(chr(tree_bytes.pop(0)))

		if ch == 49:

			root = TreeNode("IN", self.build_tree(tree_bytes), self.build_tree(tree_bytes))

		return root


	def decode(self, tree_bytes):

		self.root = self.build_tree(tree_bytes)

		return self.root