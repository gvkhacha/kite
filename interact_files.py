
# Bookkeeping has path and URL for documents
BOOKDIR = 'WEBPAGES_RAW/bookkeeping.json'

class DocID:
	def __init__(self, bookentry: str):
		""" Bookentry is the egntry inside bookkeeping.json
		that has a document ID/path to raw file, and URL """
		rawEntry = bookentry.replace('"', '').split(': ')
		self._ID = tuple(rawEntry[0].split('/'))
		self._URL = rawEntry[1]
		self._filepath = 'WEBPAGES_RAW/' + rawEntry[0]

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


def main():
	for i in readFromBook():
		DocID(i)

if __name__ == '__main__':
	main()