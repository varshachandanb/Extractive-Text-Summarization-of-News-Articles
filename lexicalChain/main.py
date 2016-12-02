import os
import json
from documentPreprocessing import document_Processing
from lexChain import LexicalChain

with open('../config.json') as data_file:
    data = json.load(data_file)
config =data

#root="/Users/vchandan/Development/TextSummarization/nlp_project/lexicalChain/temp/"

#root="/Users/vchandan/Development/TextSummarization/nlp_project/test/"
root="../Dataset/bbc-2/politics/"
percentage = config['extractPercent']
wordList=[]
chains=[]
sentences=[]

files = [os.path.join(path, filename)
            for path, dirs, files in os.walk(root)
            for filename in files
            if filename.endswith(".txt")]


for file in files:
    wordList = []
    chains = []
    sentences = []
    doc = document_Processing()
    sentences=doc.preprocessing(file)
    wordList = doc.pickNounAndLemmatize(sentences)
    lex = LexicalChain()
    chains=lex.assignChain(wordList,chains,sentences,percentage,file)



