import time
import shutil
import os 
 
dirname = r'c:\Users\warren\Downloads'
delete_older_than = [1, 1] # in seconds, always deletes older than 
percent_full_delete_threshold = 0.95 # If disk passes this threshold use second value for delete_older_than. 
incl_folders = True # Delete folders
incl_files = True # Delete files

# Should only choose one of the following options, not both
incl_file_type = ['.txt'] # Only delete files of extension type .xyz
excl_file_type = ['.txt'] # Do not delete files with extension type .xyz, overpowers whitelist

def delete_files(paths, include_folders=False, include_files=True): 
	""" Delete files and folders within the input list of form [files, folders]. """
	files, folders = paths
	for file in files:
		try: 
			os.remove(file) 
		except OSError as e: 
			print("No file error: {} - {}".format(e.filename, e.strerror))
	for folder in folders: 
		try:
			shutil.rmtree(folder)
		except OSError as e: 
			print("No folder error: {} - {}".format(e.filename, e.strerror))

def extension(paths, incl_file_type=[], excl_file_type=[]): # Work on implementing this into wrapper
	files, folders = paths
	files_to_delete = []
	for file in files:
		for file_type in incl_file_type:
			if file.lower().endswith(file_type) == True:
				files_to_delete.append(file)
		for file_type in excl_file_type: 
			if file.lower().endswith(file_type) == True:
				files_to_delete.remove(file) 
	if incl_file_type == excl_file_type == []:
		return paths # If there are no blacklist/whitelist options return original files/folder locations
	return [files_to_delete, folders]				

def older_than_decorate(func): 
	"""Decorator for the directory_list function. Wraps a file age test. """
	def wrapper(dirname, older_than = 7*24*60*60, *args, **kwargs):
		paths = func(dirname, *args, **kwargs)
		files, folders = paths
		files_older = []
		folders_older = []
		for file in files:
			file = os.path.join(dirname, file) 
			try: 
				st = os.stat(file)
				if time.mktime(time.gmtime())-st.st_mtime >= older_than: # Time measured since epoch, in UTC
					files_older.append(file)
			except FileNotFoundError as e: 
				print("Error: {} = {}".format(e.filename, e.strerror))
		for folder in folders:
			folder = os.path.join(dirname, folder) 
			try: 
				st = os.stat(folder)
				if time.mktime(time.gmtime())-st.st_mtime >= older_than: # Time measured since epoch, in UTC
					folders_older.append(folder)
			except FileNotFoundError as e: 
				print("Error: {} = {}".format(e.filename, e.strerror))
		return [files_older, folders_older] 
	return wrapper
	
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
	if disk_info[2]/disk_info[0] >= percent_full_delete_threshold:
		paths = directory_list(dirname, delete_older_than[1], incl_files, incl_folders)
	else: 
		paths = directory_list(dirname, delete_older_than[0], incl_files, incl_folders)
	paths = extension(paths, incl_file_type, excl_file_type)
	delete_files(paths, incl_folders, incl_files) 