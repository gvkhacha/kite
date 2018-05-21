from database import interact_files
from collections import defaultdict, Counter
from structures import DocID, ImgID

def searchImages(index:dict, q:str) -> list:
	try:
		return index[q].most_common()[:10]
	except:
		return index[q].most_common()


def main():
	imgIndex = interact_files.loadIndexFromFile('img')
	q = input("Give me a search query: ")
	while q != '':
		results = searchImages(imgIndex, q)
		for r in results:
			img = r[0]
			print(img.getImgURL())
			print(img.getURL())
		print('--------------')
		q = input("Give me a search query: ")

if __name__ == '__main__':
	main()
	# imgIndex = {(title, alt): [(url, value)]}