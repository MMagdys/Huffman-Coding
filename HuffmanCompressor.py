from HuffmanTree import HuffmanTree
import HuffmanHeaders
import time, os


class HuffmanCompressor(object):

	def __init__(self):

		self.encoded_txt = ""
		self.encoded_tree = bytearray()
		self.compression_bytes = bytearray()



	def get_encoded_txt(self, txt, codes):

		self.encoded_txt = ''.join([codes[ch] for ch in txt])

		return self.encoded_txt



	def encoded_arr(self, encoded_txt, encoded_tree, filename):

		trail = 8 - len(encoded_txt) % 8
		if trail:
			encoded_txt += "0"*trail


		comp_arr = bytearray()
		# first byte : number oftrailling 0s 
		comp_arr.append(trail)

		# 2->5 bytes : length of encode tree
		# 5 -> n : encode tree
		tree_arr = len(encoded_tree).to_bytes(4, byteorder="little")
		comp_arr.extend(tree_arr)
		comp_arr.extend(self.encoded_tree)

		# n-> m : file name and file extention

		comp_arr.extend(HuffmanHeaders.file_header(filename))

		data_arr = bytearray()
		data_arr.extend(int(encoded_txt,2).to_bytes((len(encoded_txt))//8, byteorder="little"))

		comp_arr.extend(data_arr)

		return comp_arr



	def compress_file_old(self, filename):

		t1 = time.time()

		with open(filename, "rb") as src:

			txt = src.read()

			tree = HuffmanTree()
			codes , self.encoded_tree = tree.huffman_coding(txt)
			# print(codes)
			self.get_encoded_txt(txt, codes)

		src.close()

		with open(filename.split('.')[0]+".huffman", "wb") as dest:
			dest.write(self.encoded_arr(self.encoded_txt, self.encoded_tree))

		dest.close()

		t2 = time.time()

		return t2 - t1, filename.split('.')[0]+".huffman"
		# return self.encoded_arr(self.encoded_txt, self.encoded_tree)



	def compress_file(self, filename):

		
		with open(filename, "rb") as src:

			txt = src.read()

			tree = HuffmanTree()
			codes , self.encoded_tree = tree.huffman_coding(txt)
			# print(codes)
			self.get_encoded_txt(txt, codes)

		src.close()

		t2 = time.time()

		return self.encoded_arr(self.encoded_txt, self.encoded_tree, filename)



	def compress_files(self, filename, path="."):

		if filename is None : filename = path
		# if comp_arr is None:
		# 	comp_arr = bytearray()

		filename = path + "/" + filename
		
		if (os.path.isdir(filename)) :

			dir_array = bytearray()

			dir_header, files = HuffmanHeaders.dir_header(filename)
			dir_array.extend(dir_header)

			self.compression_bytes.extend(dir_array)

			for file in files :
				self.compress_files(file, filename)

		else:

			self.compression_bytes.extend(self.compress_file(filename))


	def compress(self, filename):

		t1 = time.time()

		self.compress_files(filename)

		# output, ext = HuffmanHeaders.filename_split(filename)

		with open(filename.split(".")[0] + ".huffman", "wb") as dest:
			dest.write(self.compression_bytes)

		dest.close()

		t2 = time.time()



h = HuffmanCompressor()
h.compress("folder1")
# print(h.compression_bytes)
# h.compress_file("folder1/f2")