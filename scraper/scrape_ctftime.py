import logging
import urllib2
import sys, getopt
import requests
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

url = "https://ctftime.org/writeup/"



def counter(low,high):
	#for count in xrange(450,500):
	tags=""
	rating=0
	ourl=""
	with open('links.csv', 'wb') as csvfile:
		spamwriter = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
		for count in xrange(low,high+1):
			try:
				# response = urllib2.urlopen('https://ctftime.org/writeup/'+str(count))
				# html = response.read()
				response = requests.get(url+str(count),headers=headers)
				html = response.content

				if "Original writeup" in html:
					t=html.find("Original writeup")
					p=html.rfind("href=\"",0,t)
					q=html.rfind("target=",0,t)
					s=html[p+6:q-2]

					ourl = html[p+6:q-2]
				else:
					ourl = ""

				if "Rating:" in html:
					t=html.find("Rating:")
					p=html.rfind("</span></p>",t)
					rating=html[t:p].split(">")[1]
				else:
					rating=0

				if "Tags" in html:
					t=html.find("Tags")
					p=html.rfind("</span>&nbsp;",t)
					tags=html[t:p].split(">")[2].split("<")[0]
				else:
					tags=""

				print (count,"\t",ourl,"\t",rating,"\t",tags)
				spamwriter.writerow([count,ourl,rating,tags])
			except Exception as e:
				logging.exception("message")
				continue
def help_page():
	print ('writeup_browser.py -l <low_range> -h <high_range>')
	print ('Writeup browser for ctftime.org.',)
	print ('Enter the low and high range to read writeups.')
	print ('Say, if you are on https://ctftime.org/writeup/3689 and you want to',)
	print ('read next 4 writeups as well',)
	print ('then writeup_browser.py -l 3689 -h 3693')
	sys.exit(2)
def main(argv):
	inputfile = ''
	outputfile = ''
	low=0
	high=0

	try:
		opts, args = getopt.getopt(argv,"l:h:",["low=","high="])
	except getopt.GetoptError:
		help_page()
		sys.exit(2)
	if opts==[]:
		help_page()
	for opt, arg in opts:
		if opt in ("-l", "--low"):
			low = arg
	  	elif opt in ("-h", "--high"):
			high = arg
	if high<0 or low<0:
		sys.exit(2)
	low=int(low)
	high=int(high)
	if high<low:
			sys.exit(2)
	if (high-low)>10:
		print ("This will open more than 10 pages. Continue(Y/N)?")
		x=raw_input("")
		if x=='y' or x=='Y':
			pass
		elif x=='n' or x=='N':
			sys.exit(2)
	counter(low,high)
if __name__ == "__main__":
   main(sys.argv[1:])