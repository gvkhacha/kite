from html.parser import HTMLParser
from collections import defaultdict
from bs4 import BeautifulSoup, Comment
import re

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
			print(element.name)
			print('\n-------\n')
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
		parents = list(element.parents)
		weight = 0
		# print('Found text\n\tPARENTS:')
		# for i in parents:
		# 	print(i.name)
		if 'p' in parents:
			# print("JUST PARAGRAPH")
			# print('\t{}'.format(element))
			# print("PARAGRAPH END")
			self._addTextToIndex(element, 2)
		elif any([HEADERS.match(i.name) for i  in parents]):
			# print("THIS IS IMPORTANT!!!!")
			# print(element)
			# print('DONE IMPORTANT')
			self._addTextToIndex(element, 2)
	def _addTextToIndex(self, text, weight):
		"""Takes the text, tokenizes with language changes and number differences"""
		for token in text.split():
			self._index[token].append( (self._doc.getID(), weight) )