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
	if indexType == 'main':
		with open('index.pickle', 'wb') as file:
			pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
	elif indexType == 'img':
		with open('imgIndex.pickle', 'wb') as file:
			pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)
	else:
		raise Warning('Invalid function call - incorrect type defined')


def loadIndexFromFile(indexType='main') -> dict:
	if indexType == 'main':
		with open('index.pickle', 'rb') as file:
			return pickle.load(file)
	elif indexType == 'img':
		with open('imgIndex.pickle', 'rb') as file:
			return pickle.load(file)
	else:
		raise Warning('Invalid function call - incorrect type defined')

def resetIndexFiles() -> None:
	try:
		os.rename('index.pickle', 'index.pickle.bak')
		os.rename('imgIndex.pickle', 'imgIndex.pickle.bak')
	except FileNotFoundError:
		pass # File never existed in first place


def main():
	index = {'a': 5, 'b': 7, 'c':8}
	imgIndex = {'first.jpg': 'http://blah.com', 'second.png': 'http://ahaha.com'}
	# saveIndexToFile(index)
	# saveIndexToFile(imgIndex, 'img')
	testIndex = loadIndexFromFile()
	testImg = loadIndexFromFile('img')
	assert index == testIndex
	assert imgIndex == testImg

if __name__ == '__main__':
	main()