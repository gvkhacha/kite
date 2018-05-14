from structures import DocID
import pickle, os

# Bookkeeping has path and URL for documents
BOOKDIR = 'WEBPAGES_RAW/bookkeeping.json'
TMP = 2 #Change to -1 when done testing


def readFromBook():
	"""Generator that will handle opening the file and closing to 
	ensure no data loss, and yield every line in the bookkeeping file.
	"""
	TMPCOUNT = 0 #Temporary count, for init testing, we only use ~30 docs
	with open(BOOKDIR, 'r') as bf:
		for line in bf:
			if len(line) < 4: # line is { or }, ignore.
				continue
			#TMP
			TMPCOUNT += 1
			if TMP == -1 or TMPCOUNT > TMP:
				break
			#TMPEND
			yield line.strip().strip('",')

def saveIndexToFile(index: dict) -> None:
	with open('index.pickle', 'wb') as file:
		pickle.dump(index, file, protocol=pickle.HIGHEST_PROTOCOL)

def loadIndexFromFile() -> dict:
	with open('index.pickle', 'rb') as file:
		return pickle.load(file)

def resetIndexFile() -> None:
	try:
		os.rename('index.pickle', 'index.pickle.bak')
	except FileNotFoundError:
		pass # File never existed in first place


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