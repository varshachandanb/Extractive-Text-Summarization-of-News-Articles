import os,math,collections

#rootDir = "compareDir"
rootDir="../results/40"
#rootDir="/Users/vchandan/Development/TextSummarization/nlp_project/results"
#rootDir="/Users/vchandan/Development/TextSummarization/nlp_project/comparator_test"
#rootDir="/Users/vchandan/Development/TextSummarization/nlp_project/summaryUtils"
'''globalFileContent = {}
inverseDocumentFrequencies = {}
queryTerms = {}
queryVector = {}
results = {}'''
resultCSV = ""

def traverserFolder(folderPath):
    fileNames = os.listdir(folderPath)
    for fileName in fileNames:
        if not ".DS_Store" in fileName and ".txt" in fileName:
            processFiles(folderPath, fileName)

def processFiles(dirPath, fileName):
    fileAbsPath = os.path.join(dirPath, fileName)
    if not ".DS_Store" in fileName and (str(fileName)).endswith(".txt") and "sumy" not in fileName:
        fileHandler = open(fileAbsPath, "r", encoding="latin1")
        wordList = [word.strip().lower() for word in fileHandler.read().split()]
        contentDict = dict(collections.Counter(wordList))
        inverseDocumentFrequencies.update((x, 0) for x in set(wordList))
        contentDict = normalizeContentDict(contentDict)
        globalFileContent[fileAbsPath] = contentDict
        fileHandler.close()


def calculateInverseDocFrequencies():
    noOfDocs = len(globalFileContent.keys())
    for key in inverseDocumentFrequencies.keys():
        wordDocCount = 0
        for values in globalFileContent.values():
            if key in values.keys():
                wordDocCount += 1
        if wordDocCount > 0:
            inverseDocumentFrequencies[key] = 1+math.log(float((noOfDocs/wordDocCount)))
        else:
            inverseDocumentFrequencies[key] = 1


def normalizeContentDict(contentDict):
    dictValueCount = sum(contentDict.values())
    for key in contentDict.keys():
        contentDict[key] /= dictValueCount;
    return contentDict



def writeSummaryToFile(sentences,fileName):
    fileHandler = open("summaries/summary_"+fileName,"w");
    fileHandler.write(sentences)
    fileHandler.close()

def generateSumyDictionaryForQuery(folderPath):
    fileNames = os.listdir(folderPath)
    for fileName in fileNames:
        if not ".DS_Store" in fileName and ".txt" in fileName and "sumy" in fileName:
            fileAbsPath = os.path.join(folderPath, fileName)
            fileHandler = open(fileAbsPath, "r", encoding="latin1")
            wordList = set([word.strip().lower() for word in fileHandler.read().split()])
            for word in wordList:
                documentDict = {}
                for key,fileContentDict in globalFileContent.items():
                    if word in fileContentDict.keys():
                        documentDict[key] = fileContentDict[word] * inverseDocumentFrequencies[word]
                    else:
                        documentDict[key] = 0
                queryTerms[word] = documentDict
            fileHandler.close()

def generateQueryVector(folderPath):
    fileNames = os.listdir(folderPath)
    for fileName in fileNames:
        if not ".DS_Store" in fileName and ".txt" in fileName and "sumy" in fileName:
            fileAbsPath = os.path.join(folderPath, fileName)
            fileHandler = open(fileAbsPath, "r", encoding="latin1")
            wordList = [word.strip().lower() for word in fileHandler.read().split()]
            contentDict = dict(collections.Counter(wordList))
            contentDict = normalizeContentDict(contentDict)
            for key in contentDict.keys():
                if key in inverseDocumentFrequencies:
                    contentDict[key] = contentDict[key] * inverseDocumentFrequencies[key]
            queryVector.update(contentDict.items())

def cosineSimilarity(query, document2):
    numerator = 0
    queryAbsValue = 0
    doc2AbsValue = 0
    for key,value in queryTerms.items():
        doc2AbsValue += value[document2] * value[document2]
    for value in query.values():
        queryAbsValue += value * value
    doc2AbsValue = math.sqrt(doc2AbsValue)
    queryAbsValue = math.sqrt(queryAbsValue)
    denominator = queryAbsValue * doc2AbsValue
    for vectorTerm,queryVectorTermValue in query.items():
        queryTermDictionary = dict(queryTerms[vectorTerm])
        numerator += queryTermDictionary[document2] * queryVectorTermValue

    if (denominator == 0):
        return 0
    return (numerator/denominator)


pageRank_avg = 0
lexical_avg = 0
hybrid_avg = 0
lexRank_avg=0

for root, subdirs, files in os.walk(rootDir):

    globalFileContent = {}
    inverseDocumentFrequencies = {}
    queryTerms = {}
    queryVector = {}
    results = {}

    if not subdirs:
        traverserFolder(root)
        #print(root)
        # print (root + "/" +file)
        # print(globalFileContent)
        calculateInverseDocFrequencies()
        generateSumyDictionaryForQuery(root)
        '''print(inverseDocumentFrequencies)
        print("query terms \n")
        print(queryTerms)'''
        generateQueryVector(root)
        #print("Printing query vector \n")
        #print(queryVector)

        for documentName in globalFileContent.keys():
            results[documentName] = cosineSimilarity(queryVector,documentName)
            #print("Comparison of "+str(documentName)+"Value is"+str(results[documentName]))
            if("pagerank" in documentName):
                pageRank_avg = pageRank_avg + results[documentName]
            elif("hybrid" in documentName):
                hybrid_avg = hybrid_avg + results[documentName]
            elif("lexical" in documentName):
                lexical_avg = lexical_avg + results[documentName]
            elif ("lexRank" in documentName):
                lexRank_avg = lexRank_avg + results[documentName]


print ("Comparison of Hybrid with standard summarization is " + str((float)(hybrid_avg)/417))
print ("Comparison of Lexical with standard summarization is " + str((float)(lexical_avg)/417))
print ("Comparison of Pagerank with standard summarization is " + str((float)(pageRank_avg)/417))
print ("Comparison of LexRank with standard summarization is " + str((float)(lexRank_avg)/417))








