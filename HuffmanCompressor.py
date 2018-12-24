from HuffmanTree import HuffmanTree
import json
import time


class HuffmanCompressor(object):

	def __init__(self):

		self.encoded_txt = ""
		self.encoded_tree = bytearray()



	def get_encoded_txt(self, txt, codes):

		self.encoded_txt = ''.join([codes[ch] for ch in txt])

		return self.encoded_txt



	def encoded_arr(self, encoded_txt, encoded_tree):

		trail = 8 - len(encoded_txt) % 8
		if trail:
			encoded_txt += "0"*trail


		comp_arr = bytearray()
		# first byte : number oftrailling 0s 
		comp_arr.append(trail)

		# 2->5 bytes : length of encode tree
		tree_arr = len(encoded_tree).to_bytes(4, byteorder="little")
		comp_arr.extend(tree_arr)
		comp_arr.extend(self.encoded_tree)


		data_arr = bytearray()
		data_arr.extend(int(encoded_txt,2).to_bytes((len(encoded_txt))//8, byteorder="little"))

		comp_arr.extend(data_arr)

		return comp_arr



	def compress(self, filename):

		t1 = time.time()

		with open(filename, "rb") as src:

			txt = src.read()

			tree = HuffmanTree()
			codes , self.encoded_tree = tree.huffman_coding(txt)
			print(codes)
			self.get_encoded_txt(txt, codes)

		src.close()

		with open(filename.split('.')[0]+".huffman", "wb") as dest:
			dest.write(self.encoded_arr(self.encoded_txt, self.encoded_tree))

		dest.close()

		t2 = time.time()

		return t2 - t1, filename.split('.')[0]+".huffman"

