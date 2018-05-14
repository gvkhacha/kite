from html.parser import HTMLParser
from collections import defaultdict
from bs4 import BeautifulSoup, Comment


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

class Tokenizer:
	def __init__(self, doc: DocID, index: dict, imgIndex: dict):
		self._doc = doc
		self._index = index
		self._imgIndex = imgIndex
		with open(self._doc.getPath()) as htmlFile:
			self._soup = BeautifulSoup(htmlFile, 'lxml')
		self._getDocData()

	def findAllTokens(self):
		for element in self._soup.descendants:
			print(element.name)
			print('\n-------\n')
			if element.name == None:
				if element in self._comments:
					print("Found a comment!")
				else:
					print("Found some non-text comment")
					#Could check parents for importance
			elif element.name == 'img':
				self._addImage(element)

	def _getDocData(self):
		self._comments = self._soup.find_all(string=lambda text:isinstance(text,Comment))
		self._title = self._soup.title
		if self._title != None:
			self._title = self._title.text #remove <title> tag
		root = self._doc.getURL().split('/')
		if '.' in root[-1]:
			root = root[:-1]
		self._rootURL = '/'.join(root) + '/'	

	def _addImage(self, element):
		print(element.attrs)
		self._imgIndex[(self._title, element.get('alt'))].append( (self._rootURL + element['src'], 1) ) # 1 is temporary priority (?)