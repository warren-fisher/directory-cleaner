import time
import shutil
import os 
 
dirname = r'c:\Users\warren\Downloads' # drive letter and then colon, r in front denotes raw string 
dirname_unix = '' # can work with any path, ex free space in directory
delete_older_than = [3600*6, 3600*3] # in seconds, always deletes older than 
percent_full_delete_threshold = 0.95 # If disk passes this threshold use second value for delete_older_than. 
incl_folders = True
incl_files = True 

def delete_files(paths, include_folders, include_files=True): # fix for deleting folders and files 
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
		
	
def older_than_decorate(func): 
	"""Decorator for the directory_list function. Wraps a file age test. """
	def wrapper(dirname, older_than = 7*24*60*60, *args, **kwargs):
		paths = func(dirname, *args, **kwargs)
		if len(paths) == 2:
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
	if include_folders == True: 
		onlyfolders = [f for f in os.listdir(dirname) if not os.path.isfile(os.path.join(dirname, f))] 
		dir.append(onlyfolders)
	if len(dir) == 1: 
		return dir[0]
	return dir		

	
if __name__ == '__main__': 
	disk_info = shutil.disk_usage(dirname)
	if disk_info[2]/disk_info[0] >= percent_full_delete_threshold: 
		paths = directory_list(dirname, delete_older_than[1], incl_files, incl_folders)
	else: 
		paths = directory_list(dirname, delete_older_than[0], incl_files, incl_folders)
	delete_files(paths, incl_folders, incl_files) 
	
		

	
