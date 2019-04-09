import re
import logging
import urllib.request
import requests
from bs4 import BeautifulSoup
import sys
import csv

headers = requests.utils.default_headers()

headers.update( {
	"authority" : "ctftime.org",
	"cache-control" : "max-age=0",
	"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
	"accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
	"accept-language":"en-US,en;q=0.9",
	"cookie": "_ym_uid=1535248403537500351; csrftoken=lYp6NoJVuNcYLppnTg9vns20ynhCA6Ct; __atssc=google^%^3B1; __utmz=225924040.1550470046.3.3.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided); __utma=225924040.162741491.1535248402.1550808257.1553409002.5; __utmc=225924040; __utmt=1; _ym_d=1553409004; _ym_isad=1; _ym_visorc_14236711=w; __atuvc=9^%^7C8^%^2C0^%^7C9^%^2C0^%^7C10^%^2C0^%^7C11^%^2C1^%^7C12; __atuvs=5c9723ed8ae8f0de000; __utmb=225924040.2.10.1553409002"
})


def visible(element):
	if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		return False
	elif re.match('<!--.*-->', str(element.encode('utf-8'))):
		return False
	return True

def create_txt_file(uid,url,hdr):
	try:
		resp = requests.get(url,headers=hdr)
		html = resp.content
		if resp.status_code > 400:
			return False
		soup = BeautifulSoup(html,features="html.parser")
		data = soup.findAll(text=True)
		result = filter(visible, data)
		outstr = ""
		for line in result:
			outstr+=line
		outfile = open("writeup-data-web/"+uid+"-"+"web.txt","w+",encoding="utf-8")
		outfile.write(outstr)
		outfile.close()
		return True
	except Exception as e:
		logging.exception("message")
		return False

def main(argv):
	line_count=0
	with open('links.csv', 'r',encoding="utf-8") as csvfile:
		reader = csv.reader(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL) 
		for row in reader:
			if line_count == 0:
				print(f'Column names are {", ".join(row)}')
				line_count += 1
			else:
				# print(row)
				uid = row[0]
				url = row[1]
				rating = row[2]
				tags = row[3]
				hdr=None
				if "web" in tags or "web" in url:
					if url is None or len(url) == 0 or url=="":
						url = "https://ctftime.org/writeup/"+uid
						hdr=headers
					if not create_txt_file(uid,url,hdr):
						print("Failed",uid,url,tags)

if __name__ == "__main__":
	main(sys.argv[1:])