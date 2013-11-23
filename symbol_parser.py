files = ["symbols/nasdaqlisted.txt", "symbols/otherlisted.txt"]

with open("symbols/symbols.txt", "w") as output:
	for filename in files:
		with open(filename, "r") as f:
			f.readline()
			for line in f:
				parts = line.split("|")
				if len(parts[1]) != 0:
					output.write(parts[0]+"\n")
