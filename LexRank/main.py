from LexRank.documentPreprocessing import document_Processing
from LexRank.lexRank import lexRank
import os
import json

stopwords_file = "stopwords.txt"

with open('../config.json') as data_file:
    data = json.load(data_file)

config = data
root = "../Dataset/bbc-2/politics/"
percentage = config['extractPercent']

files = [os.path.join(path, filename)
            for path, dirs, files in os.walk(root)
            for filename in files
            if filename.endswith(".txt")]

for sourceFile in files:
    filteredFile = "preprocessed_text.txt"
    fileDir = sourceFile.split("/")[-1]
    fileDirName = fileDir.split(".")[0]
    resultPath = "../results/"
    if not os.path.exists(resultPath):
        os.makedirs(resultPath)
    outputPath = "../results/" +str(int(percentage*100))+"/"+fileDirName + "/"
    print(outputPath)
    if not os.path.exists(outputPath):
        os.makedirs(outputPath)
    outputFile = outputPath + "lexRank_"+ fileDirName+".txt"
    print(outputFile)
    doc = document_Processing()
    initialText = doc.preprocessing(sourceFile, filteredFile, stopwords_file)
    pageScore = lexRank()
    pageScore.calculateLexRank(filteredFile, outputFile, percentage, initialText)


