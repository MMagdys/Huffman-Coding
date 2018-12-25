from HuffmanTree import HuffmanTree
import HuffmanHeaders
import time, os


class HuffmanCompressor(object):

	def __init__(self):

		self.encoded_txt = ""
		self.encoded_tree = bytearray()
		self.compression_bytes = bytearray()



	def get_encoded_txt(self, txt, codes):

		'''
		txt(str) , codes(dict) -> encoded_txt(str)

		------------
		This Function convertes plain text "txt" into encoded 
		text using Huffman Coding "codes"

		'''

		self.encoded_txt = ''.join([codes[ch] for ch in txt])

		return self.encoded_txt



	def encoded_arr(self, encoded_txt, encoded_tree, filename):

		'''
		encoded_txt(str), encoded_tree(str), filename(str) -> comp_arr(bytearray)

		------------
		This Function takes the Huffman encoded file, the encoding tree and 
		filename to produce a bytearray consists of a header for the file so
		we can decompress it later along side with encoded file to get the 
		compressed array of the given file


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

		# m -> m+5 : length file 
		# m+5-> m + 5 + length file : encoded file 
		data_arr = bytearray()

		data_arr.extend(int(encoded_txt,2).to_bytes((len(encoded_txt))//8, byteorder="little"))
		ln = len(data_arr).to_bytes(5, byteorder="little")
		
		comp_arr.extend(ln)
		comp_arr.extend(data_arr)

		return comp_arr



	def compress_file(self, filename):

		'''
		filename(str) -> encode_arr(bytearray)

		------------
		This Function takes file name and returns its Huffman
		encode bytes array.
		'''

		with open(filename, "rb") as src:

			txt = src.read()

			tree = HuffmanTree()
			codes , self.encoded_tree = tree.huffman_coding(txt)
			# print(codes)
			self.get_encoded_txt(txt, codes)

		src.close()

		return self.encoded_arr(self.encoded_txt, self.encoded_tree, filename)



	def compress_files(self, filename, path="."):

		'''
		filename(str), path(str) -> void

		-------------
		This function gets file/directory and its relatuve 
		path (optional) traversing all files of directory 
		to compress or compress in case of file
		'''

		if filename is None : filename = path
	
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

		'''
		filename(str) -> time(time), output(str)

		--------------
		This function takes file/directory name or path 
		to compress and returns the execution time of 
		compression and output compressed file name (.huffman)
		'''

		t1 = time.time()

		self.compress_files(filename)

		output, ext = HuffmanHeaders.filename_split(filename)

		with open(output + ".huffman", "wb") as dest:
			dest.write(self.compression_bytes)

		dest.close()

		t2 = time.time()

		return (t2-t1), output+".huffman"
