import os

listOfFiles = os.listdir("Dataset//bbc-2//politics")
os.chdir("results")
for filename in listOfFiles:
   folderName = filename.split(".")[0]
   os.system ("mkdir "+str(folderName))
