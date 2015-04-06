import sys, requests, os

masterFile = open(sys.argv[1], "r")
outputFile = sys.argv[2]

chunks = []

for line in masterFile.readlines():
  if line[0:7] == "http://":
    line = line.rstrip()
    chunks.append(line)

try:
    os.stat("tmp")
except:
    os.mkdir("tmp")

os.system("chflags hidden tmp > /dev/null")

files = []
for number, chunk in enumerate(chunks):
    print "Downloading chunk "+str(number)
    data = requests.get(chunk)
    path = "tmp/"+str(number)+".ts"
    files.append(path)
    file = open(path, "a")
    file.write(data.content)
    file.close()

concat = ""

for path in files:
    concat+="file '"+path+"' \n"

chunkList = open("chunklist.txt", "a+")
chunkList.write(concat)
chunkList.close()
os.system("open chunklist.txt")
print "Joining chunks"

os.system("ffmpeg -y -f concat -i chunklist.txt -c copy -bsf aac_adtstoasc "+outputFile+" > /dev/null")
for path in files:
    os.remove(path)
os.rmdir("tmp")
os.remove("chunklist.txt")
os.system("open "+outputFile)
print "Done"