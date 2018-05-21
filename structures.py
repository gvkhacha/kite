from bs4 import BeautifulSoup, Comment
# from nltk.stem.wordnet import WordNetLemmatizer

import re

# lmtzr = WordNetLemmatizer() #Not sure, but probably better to init once.

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

class ImgID:
	def __init__(self, docid: DocID, alt: str, src: str, title: str, value):
		self._doc = docid
		self._src = src
		self._tokens = []

		weight = 30 * value
		if len(src) > 200:
			return
		for text in [title, alt, self._doc.getURL()]:
			try:
				if len(text) > 20:
					continue
				matches = re.findall(r'\w+', text.lower())
			except AttributeError:
				continue # There was no text
			except TypeError:
				continue
			for t in matches:
				self._tokens.append( (t, weight) )
			weight -= 10

	def getID(self) -> (str, str):
		return self._doc.getID()

	def getURL(self) -> str:
		return self._doc.getURL()

	def getPath(self) -> str:
		return self._doc.getPath()

	def getImgURL(self) -> str:
		return self._src

	def getTokens(self) -> list:
		return self._tokens

	def addToIndex(self, imgIndex) -> None:
		for token, weight in self._tokens:
			imgIndex[token][self] += weight


class Tokenizer:
	def __init__(self, doc: DocID, tokens: list, imgIndex: dict):
		self._doc = doc
		self._tokens = tokens
		self._imgIndex = imgIndex
		with open(self._doc.getPath()) as htmlFile:
			self._soup = BeautifulSoup(htmlFile, 'lxml')
		self._getDocData()
		#self._title, self._comments, self._rootURL

	def findAllTokens(self) -> None:
		""" Walks through all HTML elements in the document,
		checks: Comment -> skip
				Image   -> add to Img Index
				Text    -> determine weight -> add to list
		"""
		for element in self._soup.descendants:
			if element.name == None:
				if element in self._comments:
					# Ignore comments
					pass
				else:
					self._determineText(element)
			elif element.name == 'img':
				self._addImage(element)

	def _getDocData(self) -> None:
		""" Part of init. Determines documents comments, titles, and URL"""
		self._comments = self._soup.find_all(string=lambda text:isinstance(text,Comment))
		self._title = self._soup.title
		if self._title != None:
			self._title = self._title.text #remove <title> tag
		root = self._doc.getURL().split('/')
		if '.' in root[-1]:
			root = root[:-1]
		self._rootURL = '/'.join(root) + '/'	

	def _addImage(self, element) -> None:
		""" Element starts with <img> tag -> Finds details and adds 
		them to Img Index"""
		try:
			src = element['src']
		except KeyError:
			#For some reason, img doesn't have src attr *cough* WICS *cough*
			return

		alt = element.get('alt')
		if alt == None:
			alt = ''
		alt = alt.split('•')[0] # Tries to consider <img> made from snippets
		key = (self._title, alt)

		# Fix src url, considers relative and external links
		# NOT CONSIDERING PARENTS YET (?)
		if src.startswith('/'):
			srcURL = self._rootURL.split('/')[0] + element['src']
		elif 'http' in src:
			srcURL = src
		else:
			srcURL = self._rootURL + element['src']
		value = len(list(element.parents)) * 0.22
		ImgID(self._doc, alt, srcURL, self._title, value).addToIndex(self._imgIndex)


	def _determineText(self, element) -> None:
		"""Determine the weight of the text found, send to another method to 
		add to dictionary"""
		parents = list(element.parents)
		weight = 1
		parentTags = [i.name for i in parents]
		for h in ['h1','h2','h3','h4','h5','h6']:
			if h in parentTags:
				weight = int(100/int(h[-1]))
				break				
		if 'title' in parentTags:
			weight = 130
		elif 'b' in parentTags or 'i' in parentTags:
			weight = 60
		if 'script' in parentTags or 'style' in parentTags:
			# Text is in a script, can ignore
			return

		self._addTextToIndex(element, weight)

	def _addTextToIndex(self, text, weight) -> None:
		"""Takes the text, tokenizes with language changes and number differences"""
		matches = re.findall(r'\w+', text.lower())
		for i in range(len(matches)):
			try:
				int(matches[i])
				if i != 0:
					prev = "{} {}".format(matches[i-1], matches[i]).lower()
					self._tokens.append( (prev, self._doc.getID(), weight) )
				if i != len(matches) - 1:
					after = "{} {}".format(matches[i], matches[i+1]).lower()
					self._tokens.append( (after, self._doc.getID(), weight) )

			except ValueError:
				# It's not a number...
				# Lemmatizing first, not sure if thats best option yet.
				# self._tokens.append( (lmtzr.lemmatize(matches[i]), self._doc.getID(), weight) )
				# Removing lemmatization for now				
				self._tokens.append( ((matches[i], self._doc.getID(), weight))) 