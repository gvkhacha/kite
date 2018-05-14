from html.parser import HTMLParser
from collections import defaultdict

class DocID:
	def __init__(self, bookentry: str):
		""" Bookentry is the egntry inside bookkeeping.json
		that has a document ID/path to raw file, and URL """
		rawEntry = bookentry.replace('"', '').split(': ')
		self._ID = tuple(rawEntry[0].split('/'))
		self._URL = rawEntry[1]
		self._filepath = 'WEBPAGES_RAW/' + rawEntry[0]

	def getID(self) -> (str, str):
		return self._ID

	def getURL(self) -> str:
		return self._URL

	def getPath(self) -> str:
		return self._filepath

class Parser(HTMLParser):
	_tokens = defaultdict(int)
	# def handle_starttag(self, tag, attrs):
	# 	print("Encountered a start tag:", tag)

	# def handle_endtag(self, tag):
	# 	print("Encountered an end tag :", tag)

	def handle_data(self, data):
		# print("Encountered some data  :", data)
		for tok in data.split():
			# change tok, canonicalize, etc.
			self._tokens[tok.lower()] += 1
	def getTokens(self):
		return self._tokens