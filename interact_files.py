from structures import DocID
import pickle

# Bookkeeping has path and URL for documents
BOOKDIR = 'WEBPAGES_RAW/bookkeeping.json'


def readFromBook():
	"""Generator that will handle opening the file and closing to 
	ensure no data loss, and yield every line in the bookkeeping file.
	"""
	TMPCOUNT = 0 #Temporary count, for init testing, we only use ~30 docs
	with open(BOOKDIR, 'r') as bf:
		for line in bf:
			if len(line) < 4:
				continue
			#TMP
			TMPCOUNT += 1
			if TMPCOUNT > 30:
				break
			#TMPEND
			yield line.strip().strip('",')

def saveIndexToFile(index: dict) -> None:
	with open('index.pickle', 'wb') as file:
		pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)

def loadIndexFromFile() -> dict:
	with open('index.pickle', 'rb') as file:
		return pickle.load(file)


def main():
	test = dict()
	for i in readFromBook():
		x = DocID(i)
		test[x.getID()] = x.getURL()
	# saveIndexToFile(test)
	load = loadIndexFromFile()
	assert test == load

if __name__ == '__main__':
	main()