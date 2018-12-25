from HuffmanDecoder import HuffmanDecoder
import time, os

class HuffmanDecompressor(object):

	def __init__(self):

		self.root = None
		self.pln_text = []



	def get_codes(self, tree_bytes):

		'''
		tree_byte(bytesarray) -> root(TreeNode)

		------------
		This function Rebuild Huffman Tree from encoded 
		tree bytes.
		'''

		ba = bytearray()
		ba.extend(tree_bytes)
		huffman = HuffmanDecoder()
		self.root = huffman.decode(ba)



	def plain_text(self, txt_bin, root=None):

		'''
		txt_bin(binary), root(TreeNode) -> void
		Updates self.pln_text

		-----------
		This function takes binary representation of 
		Huffman encoded file and convert it to plain
		text using Huffman Tree
		'''

		for bit in txt_bin:

			if bit == "0":
				root = root.left

			elif bit == "1":
				root = root.right

			if root.left is None:
				self.pln_text += root.char
				root = self.root



	def decompress_file(self, encode_txt):

		'''
		encoded_txt(bytes array) -> void

		--------
		This function decode the file bytes using file header
		format to split the file into Huffman encoding tree, 
		file name, file extension, file path and encoded text
		in order to decompress the file and write it to disk

		header format
		-------------
		[0] byte: Number of trailing zero
		[1 : 5] bytes: length of encoded tree
		[5 : n] bytes: encoded tree
		[n : m] bytes: file name length + filename + file extension length + file extension
				HuffmanHeaders.file_header()
		[m : l] bytes: encode file length (5 bytes)
		[l : k] bytes: encoded file
		'''

		trailing = encode_txt[0]
		tree_size = encode_txt[1:5]
		tree_size = int.from_bytes(tree_size, byteorder="little")
		tree_bytes = encode_txt[5 : 5+tree_size]

		# File name size
		index = 5+tree_size
		filename_size = int.from_bytes(encode_txt[index:index+1], byteorder="little")
		filename = encode_txt[index+1:index+1+filename_size].decode("UTF-8")
		# print(filename)

		# File extension
		index = index+1+filename_size
		file_exten_size = int.from_bytes(encode_txt[index:index+1], byteorder="little")
		file_exten = encode_txt[index+1:index+1+file_exten_size].decode("UTF-8")

		# Encode Text
		index = index+1+file_exten_size

		txt_size = int.from_bytes(encode_txt[index : index+5], byteorder="little")
		# print(txt_size)
		txt_bytes = encode_txt[index + 5 : index + 5 + txt_size]
		# print(txt_bytes)
		txt_bin = format(int.from_bytes(txt_bytes, byteorder="little"), "b")[:-trailing]

		self.get_codes(tree_bytes)
		self.plain_text(txt_bin, self.root)
		self.write_file(filename, file_exten)

		index = index + 5 + txt_size
		
		if index < len(encode_txt):
			self.pln_text = ""
			self.decompress_files(encode_txt[index:])



	def write_file(self, filename, file_exten):

		'''
		filename(str), file_exten(str) -> void
		writes file

		--------------
		This function takes file name and extention to write 
		the decompressed plain data in
		'''
		
		with open(filename + file_exten, "w") as dest :

			dest.write(''.join(self.pln_text))
		dest.close()



	def decompress_files(self, compressed_file):

		'''
		compressed_file(bytes array) -> void

		--------
		This Function gets compressed file and start
		decompressing directories and files in recursive
		manner.
		''' 

		if compressed_file[:3] == b"DIR":

			name_ln = compressed_file[3]
			dir_name = compressed_file[4:4+name_ln].decode("UTF-8")
			try:
				os.mkdir(dir_name)
			except FileExistsError:
				print("[-] File Exist !")
				exit(0)

			self.decompress_files(compressed_file[4+name_ln:])

		else:
			self.decompress_file(compressed_file)



	def decompress(self, filename):

		'''
		filename(str) -> t2-t1 (time)

		----------
		This function take filename (.huffman) to decompress
		using Huffman algorthim and return the execution time
		'''

		t1 = time.time()
		with open(filename, "rb") as decomp:

			compressed_file = decomp.read()

			self.decompress_files(compressed_file)

			decomp.close()

		t2 = time.time()

		return t2 -t1
