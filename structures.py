from bs4 import BeautifulSoup, Comment
from nltk.stem.wordnet import WordNetLemmatizer

import re

lmtzr = WordNetLemmatizer() #Not sure, but probably better to init once.

HEADERS = re.compile('h[1-6]') #to add more later

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
			if element.name == None:
				if element in self._comments:
					print("Found a comment!")
				else:
					self._determineText(element)
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
		alt = element.get('alt')
		if alt == None:
			alt = ''

		key = (self._title, alt)
		src = element['src']
		if src.startswith('/'):
			baseURL = self._rootURL.split('/')[0]
		else:
			baseURL = self._rootURL
		val = (baseURL + element['src'], len(list(element.parents)) * 0.22)
		if key not in self._imgIndex:
			self._imgIndex[key].append(val)

	def _determineText(self, element):
		"""Determine the weight of the text found, send to another method to 
		add to dictionary"""
		parents = list(element.parents)
		weight = 1
		if any([HEADERS.match(i.name) for i  in parents]):
			weight = 2

		self._addTextToIndex(element, weight)

	def _addTextToIndex(self, text, weight):
		"""Takes the text, tokenizes with language changes and number differences"""
		matches = re.findall(r'\w+', text.lower())
		val = (self._doc.getID(), weight)
		for i in range(len(matches)):
			try:
				int(matches[i])
				if i != 0:
					prev = "{} {}".format(matches[i-1], matches[i]).lower()
					self._index[prev].append( val )
				if i != len(matches) - 1:
					after = "{} {}".format(matches[i], matches[i+1]).lower()
					self._index[after].append( val )

			except ValueError:
				# It's not a number...
				# Lemmatizing first, not sure if thats best option yet.

				self._index[lmtzr.lemmatize(matches[i])].append( val ) 