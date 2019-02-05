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
delete_older_than = [1, 1] # Time, in seconds, before a file is deleted. The first value applied always, the second for when your disk is atleast as full as specified.
incl_folders = True # Should this delete folders
incl_files = True # Should this delete files 

# Should probably only choose one of the following options, not both
incl_file_type = [] # Only delete files of extension type .xyz
excl_file_type = ['.txt'] # Do not delete files with extension type .xyz, overpowers whitelist

class Directory():
	"""
	A directory class is created so that class instances can be created to track user preferences of multiple directories.
	"""
	def __init__(self, path, incl_files, incl_folders, **kwargs):
		self.path = path
		self.incl_files = incl_files
		self.incl_folders = incl_folders

		disk_info = shutil.disk_usage(dirname) # Named tuple = usage(total, used, free)
		self.percent_full = disk_info[2]/disk_info[0]

		st = os.stat(self.path) # Creates a temporary named tuple

		# We run the age on __init__ because we will not save the file objects,
		# rather they will be initiated each time the script is run. 
		self.age = time.mktime(time.gmtime())-st.st_mtime # Equivalent to current_time - modified_time, in seconds

		for key, value in kwargs.items():
			setattr(self, key, value)

	def recursive_directories(self):
		"""
		Outside function to be called to initiate deleting of files. First it 
		First it checks if recursive directory mode is enabled, and if so recalls itself.  
		Once a directory is found that recursive directory mode is disabled, or the maximum search depth of 5 is reached,
		the method then calls delete_files() for all directories searched. 
		Finally if this is not the base directory we delete it, if set.
		"""
		self.get_folders()
		for folder in self.folders:
			if folder.recursive == True and folder.depth < 5: 
				folder.recursive_directories()
			elif folder.recursive == False: 
				return

		if self.incl_files == True:
			self.delete_files()

		try:
			self.depth
			if self.incl_files == True: 	
				self.delete()
		except AttributeError: 
			# If we get an attribute error we know that this is the base directory, we don't want to delete it! 
			pass 

	def get_folders(self):
		"""
		Method to list all subdirectories within the base directory.
		Creates a new class instance for each folder. 
		Not done at class initiation because it will create class instances, and therefore ages, for each folder. 
		If the age were not done at script runtime then the folder age would be outdated. 
		"""
		self.folders = [] 
		for f in os.listdir(self.path):
			if not os.path.isfile(os.path.join(self.path, f)):
				try:
					self.depth
					self.folders.append(Directory(os.path.join(self.path, f), self.incl_files, self.incl_folders, depth = self.depth+1, recursive = True))
				except AttributeError: 
					self.folders.append(Directory(os.path.join(self.path, f), self.incl_files, self.incl_folders, depth = 1, recursive = True))

	def delete_files(self):
		"""
		Method called by recursive_directories() to delete files.
		First calls get_files() to create the class attribute files, and then deletes all files older than the required age. 
		"""
		self.get_files()
		for file in self.files:
			if file.age >= delete_older_than[0]:
				file.delete()

	def get_files(self):
		"""
		Method to list all files in the base directory. 
		We only call this method when we are going to delete files because it creates class instances for each file and therefore their file age. 
		"""
		self.files = []
		for f in os.listdir(self.path):
			if os.path.isfile(os.path.join(self.path, f)):
				self.files.append(File(os.path.join(self.path, f)))

	def delete(self):
		"""
		Method to delete the directory. 
		"""
		try:
			shutil.rmtree(self.path)
		except OSError as e: # If the folder does not exist we will get this error. 
			print("No folder error: {} - {}".format(e.filename, e.strerror))

class File():
	"""
	A file class to store attributes such as age, path, and extension. 
	"""
	def __init__(self, path):
		"""
		Path is an os.path instance. 

		For finding the extension of a file if it starts with a leading period, e.g: '.gitignore', 
		the period is ignored since it's not a file extension. 
		"""
		self.path =  path
		_, self.extension = os.path.splitext(self.path) # The root of the file is not important

		st = os.stat(self.path) # Creates a temporary named tuple

		# We run the age on __init__ because we will not save the file objects,
		# rather they will be initiated each time the script is run. 
		self.age = time.mktime(time.gmtime())-st.st_mtime # Equivalent to current_time - modified_time, in seconds

	def delete(self):
		"""
		Method to delete the file.
		"""
		try: 
			os.remove(self.path) 
		except OSError as e: # If the filepath does not exist we will get this error. 
			print("No file error: {} - {}".format(e.filename, e.strerror))

if __name__ == '__main__': 
	dir = Directory(dirname, incl_files, incl_folders, recursive = True)
	dir.recursive_directories()