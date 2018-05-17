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
	def __init__(self, doc: DocID, tokens: list, imgIndex: dict):
		self._doc = doc
		self._tokens = tokens
		self._imgIndex = imgIndex
		with open(self._doc.getPath()) as htmlFile:
			self._soup = BeautifulSoup(htmlFile, 'lxml')
		self._getDocData()

	def findAllTokens(self):
		for element in self._soup.descendants:
			if element.name == None:
				if element in self._comments:
					# print("Found a comment!")
					pass
				else:
					self._determineTextWeight(element)
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
		try:
			src = element['src']
		except KeyError:
			#For some reason, img doesn't have src attr *cough* WICS *cough*
			return
		alt = element.get('alt')
		if alt == None:
			alt = ''
		alt = alt.split('•')[0]
		key = (self._title, alt)

		if src.startswith('/'):
			srcURL = self._rootURL.split('/')[0] + element['src']
		elif 'http' in src:
			srcURL = src
		else:
			srcURL = self._rootURL + element['src']
		val = (srcURL, len(list(element.parents)) * 0.22) #If there are a lot of parents, img is buried/likely not as important
		if key not in self._imgIndex:
			self._imgIndex[key].append(val)

	def _determineTextWeight(self, element):
		"""Determine the weight of the text found, send to another method to 
		add to dictionary"""
		parents = list(element.parents)
		weight = 1
		parentTags = [i.name for i in parents]
		if any([HEADERS.match(tag) for tag in parentTags]):
			weight = 2
		if 'script' in parentTags or 'style' in parentTags:
			# Text is in a script, can ignore
			return

		toAdd = self._modifyText(element, weight)
		self._addTokens(toAdd)

	def _modifyText(self, text, weight) -> [tuple]:
		"""Takes the text, tokenizes with language changes and number differences
		returns a list of (token, docID, weight) tuples"""
		result = []
		matches = re.findall(r'\w+', text.lower())
		for i in range(len(matches)):
			try:
				int(matches[i])
				if i != 0:
					prev = "{} {}".format(matches[i-1], matches[i]).lower()
					result.append( (prev, self._doc.getID(), weight) )
				if i != len(matches) - 1:
					after = "{} {}".format(matches[i], matches[i+1]).lower()
					result.append( (after, self._doc.getID(), weight) )

			except ValueError:
				# It's not a number...
				# Lemmatizing first, not sure if thats best option yet.
				# self._tokens.append( (lmtzr.lemmatize(matches[i]), self._doc.getID(), weight) )
				# Removing lemmatization for now		
				result.append( ((matches[i], self._doc.getID(), weight))) 
		return result

	def _addTokens(self, toAdd: list) -> None:
		""" Takes a list of (token, docID, weight) pairs and adds them all to a tokens list while considering
		duplicate token, docID and just adding weight"""
		for tok, doc, weight in toAdd:
			found = False
			for i in range(len(self._tokens)):
				if self._tokens[i][0] == tok and self._tokens[i][1] == doc:
					self._tokens[i] = (tok, doc, self._tokens[i][2] + weight)
					found = True
			if not found:
				self._tokens.append((tok, doc, weight))
