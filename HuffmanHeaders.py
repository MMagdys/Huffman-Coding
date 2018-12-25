import os
from os import listdir, walk

def dir_header(dir_name):

	dir_header = bytearray()

	# First 3 bytes DIR (Type Identifer)
	dir_header.extend(bytes("DIR", "UTF-8"))

	# Second Filenam len and filename
	dir_name = bytes(dir_name, "UTF-8")
	dir_name_size = len(dir_name).to_bytes(1, byteorder="little")

	dir_header.extend(dir_name_size)
	dir_header.extend(dir_name)

	files = ls(dir_name)

	return dir_header, files



def ls(dir_name):

	files = os.listdir(dir_name)
	files = [file.decode("utf-8") for file in files]

	return files




def ls_fd(dir_name):

	files = []
	dirs = []

	for (dir_path, dir_names, file_names) in walk(dir_name):
		dirs.extend(dir_names)
		files.extend(file_names)

	return files, dirs



def file_header(full_filename):

	filename , file_exten = filename_split(full_filename)
	# print(filename)

	header_arr = bytearray()

	# Filenam len and filename
	filename = bytes(filename, "UTF-8")
	filename_size = len(filename).to_bytes(1, byteorder="little")

	header_arr.extend(filename_size)
	header_arr.extend(filename)

	# Filename extention
	file_exten = bytes(file_exten, "UTF-8")
	file_exten_size = len(file_exten).to_bytes(1, byteorder="little")

	header_arr.extend(file_exten_size)
	header_arr.extend(file_exten)

	return header_arr



def filename_split(full_filename):

	filename, file_exten = os.path.splitext(full_filename)

	return filename, file_exten

