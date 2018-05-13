from structures import DocID
from collections import defaultdict

import interact_files

import sys


def main(index: dict):
	print(index)


if __name__ == '__main__':
	if len(sys.argv) == 1:
		index = interact_files.loadIndexFromFile()
	elif sys.argv[1] in {'-r', 'reload'}:
		index = defaultdict(list)
		interact_files.resetIndexFile()
	else:
		raise Warning("Invalid command line input")

	try:
		main(index)
	except KeyboardInterrupt:
		pass
	finally:
		interact_files.saveIndexToFile(index)