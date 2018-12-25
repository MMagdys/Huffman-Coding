import argparse, os
from HuffmanCompressor import HuffmanCompressor
from HuffmanDecompressor import HuffmanDecompressor


def main():

	parser = argparse.ArgumentParser(description = "HUffman Algorithm for Compression and Decompression",\
	 usage="Huffman.py [action] FilePath")

	parser.add_argument("-c", "--compress", type=str, help="compress")
	parser.add_argument("-d", "--decompress", type=str, help="decompress")

	args = parser.parse_args()

	if args.compress:
		
		huffman = HuffmanCompressor()
		exec_time , output = huffman.compress(args.compress)
		input_size = os.stat(args.compress).st_size
		output_size = os.stat(output).st_size
		ratio = output_size * 100 /input_size
		
		print("[+] %s : created successfully."%output)
		print("[+] Compression finished in %.5f seconds"% exec_time )
		print("[+] Compression ratio  %.1f"% ratio )


	elif args.decompress:
		
		huffman = HuffmanDecompressor()
		exec_time = huffman.decompress(args.decompress)

		print("[+] Decompression finished in %.5f seconds"% exec_time )



if __name__ == '__main__':
	main()