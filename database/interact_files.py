from structures import DocID
import pickle, os

# Bookkeeping has path and URL for documents
BOOKDIR = 'WEBPAGES_RAW/bookkeeping.json'

def readFromBook():
	"""Generator that will handle opening the file and closing to 
	ensure no data loss, and yield every line in the bookkeeping file.
	"""
	with open(BOOKDIR, 'r') as bf:
		for line in bf:
			if len(line) < 4: # line is { or }, ignore.
				continue
			yield line.strip().strip('",')

def saveIndexToFile(index: dict, indexType='main') -> None:
	"""Saves any object (index) to ./database/TYPE_index.pickle"""
	try:
		with open('database/{}_index.pickle', 'wb') as file:
			pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
	except:
		raise #re-raise fo rnow.

def loadIndexFromFile(indexType='main') -> dict:
	""" Loads and returns and object from pickled file in previous
	format - ./database/TYPE_index.pickle"""
	try:
		with open('database/{}_index.pickle', 'rb') as file:
			return pickle.load(file)
	except:
		raise #re-raise for now.


def resetIndexFiles() -> None:
	try:
		for file in os.listdir('database/'):
			if file.endswith('.pickle'):
				print("Found one")
				p = os.path.join("database/", file)
				os.rename(p, '{}.bak'.format(p))
				# os.rename(file, '{}.bak'.format(file))
		# os.rename('database/index.pickle', 'database/index.pickle.bak')
		# os.rename('database/imgIndex.pickle', 'database/imgIndex.pickle.bak')
	except FileNotFoundError:
		pass # File never existed in first place


def main():
	# index = {'a': 5, 'b': 7, 'c':8}
	# imgIndex = {'first.jpg': 'http://blah.com', 'second.png': 'http://ahaha.com'}
	# # saveIndexToFile(index)
	# # saveIndexToFile(imgIndex, 'img')
	# testIndex = loadIndexFromFile()
	# testImg = loadIndexFromFile('img')
	# assert index == testIndex
	# assert imgIndex == testImg
	resetIndexFiles()

if __name__ == '__main__':
	main()