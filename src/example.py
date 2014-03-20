from bs4 import BeautifulSoup
import urllib2, urllib, zipfile
import unicodedata

url = "http://meps.ahrq.gov/data_stats/download_data_files_codebook.jsp?PUFId=H147&sortBy=Start"
soup = BeautifulSoup(urllib2.urlopen(url).read())

for found in soup.find_all("tr",{"id":"faqRoll_neoTD3"}):
	text = unicodedata.normalize('NFKD',found.text).encode("ascii",'ignore')
	details = text.strip().replace("   ","").split("\n")
