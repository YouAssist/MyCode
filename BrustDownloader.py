import os,bs4,requests
import re

"""
This Script Downloads all The Images of given name available in Burst Website
And Saves it in a different Folder!
"""

class OtherFuncs:
	def __init__(self):
		pass
	def urlShortner(self,urls):
		shorturls = []
		for url in urls:
			try:
				ind = url.index('?')
				url = url[:ind]
				shorturls.append(url)
			except:
				pass
		return shorturls

	def LastPage(self,url):
		print(url)
		text = url
		pat = re.compile(r'\d+')
		res = pat.findall(text)
		return int(res[0])

	def TotalPages(self,url):
		res = requests.get(url)
		res.raise_for_status()
		#print(res.text)
		soup = bs4.BeautifulSoup(res.text,features="html.parser")
		try:
			FinalPage = soup.find('li', { "class" : "last"}).a.get('href')
			finalpagenum = self.LastPage(FinalPage)
		except:
			finalpagenum = 1
		return int(finalpagenum)
	
	def Pagesiter(self,reverse_Y_N):
		total_p = self.TotalPagesD
		if reverse_Y_N and total_p>1:
			pages = list(tuple(range(1,total_p+1)))
			pages.reverse()
		else:
			pages = list(tuple(range(1,total_p+1)))
		return pages



class Downloader(OtherFuncs):
	"""A class to download data"""
	def __init__(self,FileName='',reverseD = False):
		super().__init__()
		self.FileName = FileName
		if ' ' in self.FileName:
			self.Filename = self.FileName.replace(' ','+')
		self.MainDir = r'E:\My_Downloader'
		self.url = r'https://burst.shopify.com/photos/search?utf8=%E2%9C%93&q={:s}&button='.format(self.FileName) if FileName != '' else r'https://burst.shopify.com/photos'
		print(self.url)
		self.reverseD = reverseD
		self.TotalPagesD = self.TotalPages(self.url)
		self.pagenumbers = self.Pagesiter(self.reverseD)

		while True:
			for num in self.pagenumbers:
				self.url = r'https://burst.shopify.com/photos/search?button=&page={:d}&q={:s}'.format(num,self.FileName)
				res = requests.get(self.url)
				res.raise_for_status()
				soup = bs4.BeautifulSoup(res.text,features="html.parser")
				PicElem = soup.findAll('button', { "class" : "js-download-premium js-open-contextual-subscribe-modal-on-third marketing-button photo-tile__action js-track-photo-stat-click tile__overlay-trigger"})
				TotalImages = soup.find('h1', { "class" : "section-heading__heading heading--1 heading--2"}).text
				print(TotalImages,sep='\n')	
				imageurl = []
				for url in PicElem:
					imageurl.append(url.attrs["data-modal-image-url"])
				#PicElem = soup.select('a.VGpNw eBVId zGyUV _2WvKc _1cnsH _2_Uh9 okwIh _1C5V3 untracked')
				urls = self.urlShortner(imageurl)
				#print(urls)
				if urls != []:
					print('Found {:d} Files in This Page! '.format(len(urls)))
					creatfold = self.MainDir+'\\'+self.FileName
					os.makedirs(creatfold,exist_ok=True)
					os.chdir(self.MainDir+'\\'+FileName)
					for image in urls:
						if os.path.exists(os.path.basename(image)):
							print('File Already Existed '+os.path.basename(image))
						else:
							filename = open(os.path.basename(image),'wb')
							print(image)
							file = requests.get(image)
							for chunk in file.iter_content(1000000):
								filename.write(chunk)
							filename.close()
			print('Downloaded All The Pic')
			break



if __name__=='__main__':
	name = input('Enter The Picture Type: ')
	DownloaderObj = Downloader(FileName=name)
	
