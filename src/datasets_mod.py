import os, json

f1 = open("datasets/Sentences_100Agree.txt", "r").read()
f2 = open("datasets/Sentences_75Agree.txt", "r").read()
f3 = open("datasets/Sentences_66Agree.txt", "r").read()
f4 = open("datasets/Sentences_50Agree.txt", "r").read()

ds100 = {'positive':[], 'negative':[], 'neutral': []}
ds75 = {'positive':[], 'negative':[], 'neutral': []}
ds66 = {'positive':[], 'negative':[], 'neutral': []}
ds50 = {'positive':[], 'negative':[], 'neutral': []}

for line in f1.split("\n"):
	if not "@" in line:
		print line
		continue
	line = line.decode('ascii', 'ignore')
	ds100[line.split("@")[1].strip()].append(line.split("@")[0].strip())
for line in f2.split("\n"):
	if not "@" in line:
		print line
		continue
	line = line.decode('ascii', 'ignore')
	ds75[line.split("@")[1].strip()].append(line.split("@")[0].strip())
for line in f3.split("\n"):
	if not "@" in line:
		print line
		continue
	line = line.decode('ascii', 'ignore')
	ds66[line.split("@")[1].strip()].append(line.split("@")[0].strip())
for line in f4.split("\n"):
	if not "@" in line:
		print line
		continue
	line = line.decode('ascii', 'ignore')
	ds50[line.split("@")[1].strip()].append(line.split("@")[0].strip())

f11 = open("datasets/ds100.json", "w")
f22 = open("datasets/ds75.json", "w")
f33 = open("datasets/ds66.json", "w")
f44 = open("datasets/ds50.json", "w")

json.dump(ds100, f11)
json.dump(ds75, f22)
json.dump(ds66, f33)
json.dump(ds50, f44)

f11.close()
f22.close()
f33.close()
f44.close()