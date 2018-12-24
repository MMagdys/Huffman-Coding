from HuffmanDecoder import HuffmanDecoder
import time

class HuffmanDecompressor(object):

	def __init__(self):

		self.root = None
		self.pln_text = []



	def get_codes(self, tree_bytes):

		ba = bytearray()
		ba.extend(tree_bytes)
		huffman = HuffmanDecoder()
		self.root = huffman.decode(ba)



	def plain_text(self, txt_bin, root=None):
		

		for bit in txt_bin:

			if bit == "0":
				root = root.left

			elif bit == "1":
				root = root.right

			if root.left is None:
				# print(self.pln_text , root.char)
				# self.pln_text.append(root.char)
				self.pln_text += root.char
				root = self.root



	def decompress(self, filename):

		t1 = time.time()
		with open(filename, "rb") as decomp:

			encode_txt = decomp.read()

			trailing = encode_txt[0]
			tree_size = encode_txt[1:5]
			tree_size = int.from_bytes(tree_size, byteorder="little")
			tree_bytes = encode_txt[5 : 5+tree_size]

			txt_bytes = encode_txt[5+tree_size : ]
			txt_bin = format(int.from_bytes(txt_bytes, byteorder="little"), "b")[:-trailing]

			self.get_codes(tree_bytes)
			self.plain_text(txt_bin, self.root)
			# print(encode_txt)
			# print(tree_bytes)
			# print(txt_bin)
			# print(self.pln_text)

			decomp.close()

			with open(filename.split(".")[0]+"_decomp", "w") as dest :

				dest.write(''.join(self.pln_text))

				dest.close()

		t2 = time.time()

		return (t2-t1)
