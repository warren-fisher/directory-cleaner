import time
import shutil
import os 
 
"""
The following are user settings. 

Dirname should be equal to r'your_path'

percent_full_delete_threshold is a float value between 0 and 1 to be used as a percentage threshold until we allow files to be less old before deleting.

delete_older_than is the list responsible for deciding how old a file has to be before being deleted.
The first value applies always and the second value applied for when the disk is more than x% full as set in percent_full_delete_threshold

incl_folders and incl_files are for setting whether script will delete folders, files or both 
"""
dirname = r'c:\Users\warren\Downloads'
percent_full_delete_threshold = 0.95 # If disk passes this threshold use second value for delete_older_than. 
delete_older_than = [60*60*24*30, 60*60*24*15] # Time, in seconds, before a file is deleted. The first value applied always, the second for when your disk is atleast as full as specified.
incl_folders = True # Should this delete folders
incl_files = True # Should this delete files 

# Should probably only choose one of the following options, not both
incl_file_type = [] # Only delete files of extension type .xyz
excl_file_type = ['.txt'] # Do not delete files with extension type .xyz, overpowers whitelist

def delete_files(paths, include_folders=False, include_files=True): 
	""" Delete files and folders within the input list of form [files, folders]. """
	files, folders = paths
	for file in files:
		try: 
			os.remove(file) 
		except OSError as e: # If the file does not exist we will get this error. 
			print("No file error: {} - {}".format(e.filename, e.strerror))
	for folder in folders: 
		try:
			shutil.rmtree(folder)
		except OSError as e: # If the folder does not exist we will get this error. 
			print("No folder error: {} - {}".format(e.filename, e.strerror))

def extension(paths, incl_file_type=[], excl_file_type=[]): # Work on implementing this into wrapper
	files, folders = paths
	files_to_delete = []
	if incl_file_type == excl_file_type == []:
		return paths # If there are no blacklist/whitelist options return original files/folder locations
	for file in files:
		if incl_file_type == []: 
			files_to_delete = files
		else:
			for file_type in incl_file_type:
				if file.lower().endswith(file_type) == True:
					files_to_delete.append(file)
		for file_type in excl_file_type: 
			try:
				if file.lower().endswith(file_type) == True:
					files_to_delete.remove(file)
			except ValueError:
			# If a file is not in the files_to_delete list it will throw this error.
			# This can happen if a user sets a whitelist as well as a blacklist with different file extension types. 
				print("Error: You set a whitelist and blacklist at the same time, which is not recommended") 
	return [files_to_delete, folders]				

def older_than_decorate(func): 
	"""Decorator for the directory_list function. Wraps a file age test. """
	def wrapper(dirname, older_than = 7*24*60*60, *args, **kwargs):
		paths = func(dirname, *args, **kwargs) # Call our directory_list function to return a list of all files and folders (non-recursive) in format [filers, folders].
		files, folders = paths
		files_older = []
		folders_older = []
		for file in files:
			file = os.path.join(dirname, file) # Gives us the absolute path of a file 
			try: 
				st = os.stat(file)
				if time.mktime(time.gmtime())-st.st_mtime >= older_than: # The left hand side equates to the age, in seconds, of a file
					files_older.append(file)
			except FileNotFoundError as e: 
				print("Error: {} = {}".format(e.filename, e.strerror))
		for folder in folders:
			folder = os.path.join(dirname, folder) 
			try: 
				st = os.stat(folder)
				if time.mktime(time.gmtime())-st.st_mtime >= older_than: # The left hand side equates to the age, in seconds, of a file
					folders_older.append(folder)
			except FileNotFoundError as e: 
				print("Error: {} = {}".format(e.filename, e.strerror))
		return [files_older, folders_older] # Returns folders and files older than the desired age. 
	return wrapper # Returns the wrapper function so that when we decorate it to directory_list it is called instead of it. 
	
@older_than_decorate
def directory_list(dirname, include_files = True, include_folders = False): 
	"""List all files and or sub-directories within a directory. Will not recursively list all files within sub-directories.""" 
	dir = [] 
	if include_files == True: 
		onlyfiles = [f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))]
		dir.append(onlyfiles)
	else:
		dir.append([]) # Append empty list so that it appears there are no files to delete.
	if include_folders == True: 
		onlyfolders = [f for f in os.listdir(dirname) if not os.path.isfile(os.path.join(dirname, f))] 
		dir.append(onlyfolders)
	else:
		dir.append([]) # Append empty list so that it appears there are no folders to delete.
	return dir		

if __name__ == '__main__': 
	disk_info = shutil.disk_usage(dirname) # Named tuple usage(total, used, free)
	try:
		int(percent_full_delete_threshold)
		if disk_info[2]/disk_info[0] >= percent_full_delete_threshold:
			paths = directory_list(dirname, delete_older_than[1], incl_files, incl_folders)
		else: 
			paths = directory_list(dirname, delete_older_than[0], incl_files, incl_folders)
	except ValueError: # If percent_full_delete_threshold is not an integer than we know the user does not want that feature enabled. Act like it wasnt full enough. 
		paths = directory_list(dirname, delete_older_than[0], incl_files, incl_folders)
	paths = extension(paths, incl_file_type, excl_file_type)
	delete_files(paths, incl_folders, incl_files) 