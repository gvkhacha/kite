import interact_files
from structures import DocID
from collections import defaultdict, Counter
import json, pickle

def getDocIDs() -> dict:
	with open('bookkeeping.json', 'r') as file:
		return json.loads(file.read())

def main():
	index = interact_files.loadIndexFromFile('main')
	docs = getDocIDs()
	newIndex = defaultdict(Counter)
	for k, v in index.items():
		try:
			for doc, freq in v.items():
				dstring = "{}/{}".format(doc[0], doc[1])
				s = '    "{}": "{}"'.format(dstring, docs[dstring])
				x = DocID(s)
				newIndex[k][x] += freq
		except AttributeError:
			pass
	with open('index_docID.pickle', 'wb') as file:
		pickle.dump(newIndex, file, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
	main()