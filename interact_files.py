
# Bookkeeping has path and URL for documents
BOOKDIR = 'WEBPAGES_RAW/bookkeeping.json'

class DocID:
	def __init__(self, bookentry: str):
		""" Bookentry is the egntry inside bookkeeping.json
		that has a document ID/path to raw file, and URL """
		print(bookentry)

def readFromBook():
	"""Generator that will handle opening the file and closing to 
	ensure no data loss, and yield every line in the bookkeeping file.
	"""
	TMPCOUNT = 0 #Temporary count, for init testing, we only use ~30 docs
	with open(BOOKDIR, 'r') as bf:
		for line in bf:
			#TMP
			TMPCOUNT += 1
			if TMPCOUNT > 30:
				break
			#TMPEND

			yield line.strip().strip(',')


def main():
	for i in readFromBook():
		DocID(i)

if __name__ == '__main__':
	main()