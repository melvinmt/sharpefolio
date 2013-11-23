import urllib2

files = ["nasdaqlisted.txt", "otherlisted.txt"]

for filename in files:
	contents = urllib2.urlopen("ftp://ftp.nasdaqtrader.com/SymbolDirectory/"+filename)
	with open("symbols/"+filename, "w") as f:
		[f.write(x) for x in contents.read()]
