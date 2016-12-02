from documentPreprocessing import document_Processing
from pageRank import page_Rank
import os
import json

with open('../config.json') as data_file:
    data = json.load(data_file)
config = data

source_file = "InputFile.txt"
sentence_Filtered_File = "preprocessed_text.txt"
targetFile = "TargetFile1.txt"
stopwords_file = "stopwords.txt"
max = 3

for root, subdirs, files in os.walk("../Dataset/bbc-2/politics/"):
    if not subdirs:
        for file in files:
            doc = document_Processing()
            doc.preprocessing(root + "/" + file, sentence_Filtered_File, stopwords_file)
            pageScore = page_Rank()
            folderName = file.split(".")[0]
            pageScore.calculatePageRank(sentence_Filtered_File, "../results/"+str(int(config['extractPercent']*100))+"/" + folderName + "/pagerank_" + file, max)






