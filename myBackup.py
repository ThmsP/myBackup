import os
import multiprocessing as mp
import hashlib

class fichier():

	def  __init__(self, path_up, name):
		self._name = name
		self._path = path_up
		if not os.path.isdir(self.getPath()) :
			self._md5 = md5Checksum(self.getPath())

	def __eq__(self, objet):
		return (self.getmd5Sum() == objet.getmd5Sum()) and (self.getPath() != objet.getPath())

	def getParentDir(self):
		return self._path.split('/')[-1]

	def getmd5Sum(self):
		return self._md5

	def getPath(self):
		return self._path+'/'+self._name

	def show(self):
		print 'This is file %s md5sum : %s '%(self.getPath(),self._md5)



class dossier(fichier):

	def __init__(self, path_up, name):
		fichier.__init__(self,path_up, name)
		self._attached_file = []
		self._attached_dir = []

	def attach(self, obj):
		if os.path.isdir(obj.getPath()) :
			self._attached_dir.append(obj)
		else : 
			self._attached_file.append(obj)

	def getAttached(self):
		return (i for i in self._attached_file), (j for j in self._attached_dir)

	def dirExist():
		return True

	def show(self):
		print 'This is dir %s \n '%(self.getPath())
		print 'File and Dir inside :\n'
		print '%s'%(self._attached_file)
		print '%s'%(self._attached_dir)

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

paths = ['/home/thms/Dev/Python/recursive_save/current', '/home/thms/Dev/Python/recursive_save/backup']

# Define an output queue
output = [mp.Queue(), mp.Queue()]

results_current = []
results_save = []

def walk_tuple(path1, out):
	for path, dirs, files in os.walk(path1):
		sortie= []
		sortie.append([path, dirs, files])
		out.put(sortie)

def identifySameFile(files_l, same_fi_l):
	files_l_out = files_l
	for i in files_l:
		temp = []
		for j in files_l:
			if i == j :
				temp.append(j)
				files_l_out.pop(files_l.index(j))
		if temp != [] :
			temp.append(i)
			same_fi_l.append(temp)
			files_l_out.pop(files_l.index(i))
			return False, same_fi_l, files_l_out
	return True, same_fi_l, files_l_out

process_current = mp.Process(target=walk_tuple, args=(paths[0],output[0]))
process_backup  = mp.Process(target=walk_tuple, args=(paths[1],output[1]))
# 
process_current.start()
process_backup.start()

process_current.join()
process_backup.join()

while not output[0].empty():
	results_current.append(output[0].get()) 
while not output[1].empty():
	results_save.append(output[1].get())

# print results_save
# print results_current

dirs_list_current = mp.Queue()
files_list_current = mp.Queue()
dirs_list_backup = mp.Queue()
files_list_backup = mp.Queue()

def getDirsAndFilesListes(results, dirs_list, files_list):
	for i in results :
		# print i
		for path, dirs, files in i:
			temp = path.split('/')
			current_dir = temp.pop(len(temp)-1)
			current_dir_path = '/'.join(temp)
			d = dossier(current_dir_path, current_dir)
			for j in files:
				f = fichier(path, j)
				# f.show()
				d.attach(f)
				files_list.append(f)
			# d.show()
			dirs_list.append(d)
	

process_current = mp.Process(target=getDirsAndFilesListes, args=(results_save,dirs_list_backup, files_list_backup))
process_backup  = mp.Process(target=getDirsAndFilesListes, args=(results_current, dirs_list_current, files_list_current))
# 
process_current.start()
process_backup.start()

process_current.join()
process_backup.join()

print dirs_list_current
print dirs_list_backup
print files_list_current
print files_list_backup

###############
# same_fi_list = []
# f_list = files_list
# test = False
# while test == False:
# 	test, same_fi_list, f_list = identifySameFile(f_list, same_fi_list)
			
# print 'Same files :'
# [j.show() for i in same_fi_list for j in i ]





# define a example function
# def rand_string(length, output):
#     """ Generates a random string of numbers, lower- and uppercase chars. """
#     rand_str = ''.join(random.choice(
#                     string.ascii_lowercase
#                     + string.ascii_uppercase
#                     + string.digits)
#                for i in range(length))
#     output.put(rand_str)

# Setup a list of processes that we want to run
# processes = [mp.Process(target=walk_tuple, args=(path[x], output)) for x in range(2)]

# print 'processes ', processes

# # Run processes
# for p in processes:
#     p.start()

# # Exit the completed processes
# for p in processes:
#     p.join()

# # Get process results from the output queue
# results = [output.get() for p in processes]

# print(results)