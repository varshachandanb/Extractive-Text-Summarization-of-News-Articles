import os,math,collections
import re
import json

globalFileContent = {}
inverseDocumentFrequencies = {}
queryTerms = {}
queryVector = {}
results = {}
stopWordList = []
cueWordList = []
config = {}
sentenceLength20PercentScore = 1
sentenceLength40PercentScore = 0.75
sentenceLengthOthersScore = 0.5

sentencePositionLowerBound = 0.3
sentencePositionUpperBound = 0.7

evalWeight_tfScores = 0.8
evalWeight_titleIntersection = 0.05
evalWeight_sentencePosition = 0.05
evalWeight_sentenceLength = 0.05
evalWeight_sentenceCueWord = 0.05

extractPercent = 0
config = {}
data = ""

with open('../config.json') as data_file:
    data = json.load(data_file)
config =data

rootDir = "../Dataset/bbc-2/politics/"
#rootDir = "D:\\shiva\\nlp\\nlp_project\\test"

for word in open("stopWords.txt").readlines():
    stopWordList.append(word.strip())

for word in open("cueWords.txt").readlines():
    cueWordList.append(word.strip())

#stopWordList = [i.strip().split() for i in ]

def removeStopWords(wordList):
    for word in wordList:
        if re.sub('\W+','', word ) in stopWordList:
            wordList.remove(word)
    return wordList

def traverserFolder(folderPath):
    fileNames = os.listdir(folderPath)
    for fileName in fileNames:
        if not ".DS_Store" in fileName and ".txt" in fileName:
            processFiles(folderPath, fileName)

def processFiles(dirPath, fileName):
    fileAbsPath = os.path.join(dirPath, fileName)
    if not ".DS_Store" in fileName and (str(fileName)).endswith(".txt"):
        fileHandler = open(fileAbsPath, "r", encoding="latin1")
        wordList = [word.strip().lower() for word in fileHandler.read().split()]
        wordList = removeStopWords(wordList)
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

def generateSummary(folderPath):
    fileNames = os.listdir(folderPath)
    for fileName in fileNames:
        if not ".DS_Store" in fileName and ".txt" in fileName:
            fileAbsPath = os.path.join(folderPath, fileName)
            summary = generateIndividualSummary(fileAbsPath)
            folderName = fileName.split(".")[0]
            summary = summary.replace("\n","")
            print("../results/"+str(int(config['extractPercent']*100))+"/"+folderName+"/hybrid_"+fileName)
            writeSummaryToFile("../results/"+str(int(config['extractPercent']*100))+"/"+folderName+"/hybrid_"+fileName, summary)


def generateIndividualSummary(fileAbsPath):
    fileHandler = open(fileAbsPath, "r", encoding="latin1")
    fileContent = fileHandler.read()
    articleWords = removeStopWords((fileContent.split("\n",1)[0]).split())
    articleContent = fileContent.split("\n",1)[1]
    sentences = splitParagraphIntoSentences(articleContent)
    sentenceScoreMap, sentenceArticleIntersectionMap, sentencePositionWeighMap, sentenceLengthMap, sentenceCueWordLengthMap\
        = getSentenceScoreMap(sentences, globalFileContent[fileAbsPath], articleWords)
    summary = integrateSentence(sentences, sentenceScoreMap, sentenceArticleIntersectionMap, sentencePositionWeighMap, sentenceLengthMap, sentenceCueWordLengthMap)
    return summary

def splitParagraphIntoSentences(paragraph):
    paragraph = paragraph.strip()
    sentenceEnders = re.compile('[.!?]')
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList

def getSentenceScoreMap(sentences, wordScores, articleWords):
    sentencePosition = 0
    sentenceScoreMap = dict()
    sentenceTitleIntersectionCountMap = dict()
    sentencePositionMap = dict()
    sentenceLengthMap = dict()
    sentenceCueWordLengthMap = dict()
    for sentence in sentences:
        sentenceScoreMap[sentence] = getSentenceWeight(sentence, wordScores)
        sentenceTitleIntersectionCountMap[sentence] = getSentenceTitleIntersection(sentence, articleWords)
        sentencePositionMap[sentence] = sentencePosition
        sentencePosition += 1
        sentenceCueWordLengthMap[sentence] = getSentenceCueWordCount(sentence)
    sentenceTitleIntersectionCountMap = normalizeDictContentBySize(sentenceTitleIntersectionCountMap)
    sentenceCueWordLengthMap = normalizeDictContentBySize(sentenceCueWordLengthMap)
    sentenceLengthMap = getSentenceLengthWeightMap(sentences)
    sentencePositionWeighMap = getSentencePositionWeightMap(sentencePositionMap)
    return sentenceScoreMap, sentenceTitleIntersectionCountMap, sentencePositionWeighMap, sentenceLengthMap, sentenceCueWordLengthMap

def getSentenceWeight(sentence, wordScores):
    weight = 0
    words = sentence.split()
    for word in words:
        if word in wordScores:
            weight += wordScores[word]
    return weight

def getSentenceTitleIntersection(sentence, articleWords):
    count = 0;
    sentenceWords = sentence.split()
    for articleWord in articleWords:
        if articleWord in sentenceWords:
            count += 1
    return count

def getSentenceCueWordCount(sentence):
    count = 0;
    sentenceWords = sentence.split()
    for cueWord in cueWordList:
        if cueWord in sentenceWords:
            count += 1
    return count

def normalizeDictContentBySize(dictionary):
    dictCount = len(dictionary.items())
    for key, value in dictionary.items():
        dictionary[key] = dictionary[key]/dictCount
    return dictionary

def getSentenceLengthWeightMap(sentences):
    sentenceLengthWeightMap = dict()
    totalLength = 0
    for sentence in sentences:
        totalLength += len(sentence.split())
    averageSentenceLength = totalLength/len(sentences)
    lb_20percent = 0.8 * averageSentenceLength
    ub_20percent = 1.2 * averageSentenceLength
    lb_40percent = 0.6 * averageSentenceLength
    ub_40percent = 1.4 * averageSentenceLength
    for sentence in sentences:
        sentenceLength = len(sentence.split())
        if sentenceLength >= lb_20percent and sentenceLength <= ub_20percent:
            sentenceLengthWeightMap[sentence] = sentenceLength20PercentScore
        elif sentenceLength >= lb_40percent and sentenceLength <= ub_40percent:
            sentenceLengthWeightMap[sentence] = sentenceLength40PercentScore
        else :
            sentenceLengthWeightMap[sentence] = sentenceLengthOthersScore

    return sentenceLengthWeightMap

def getSentencePositionWeightMap(sentencesPositionMap):
    sentencePositionWeightMap = dict()
    sentenceCount = len(sentencesPositionMap.items())
    for sentence, position in sentencesPositionMap.items():
        if position <= sentencePositionLowerBound * sentenceCount   or position >= sentencePositionUpperBound * sentenceCount:
            sentencePositionWeightMap[sentence] = 1
        else :
            sentencePositionWeightMap[sentence] = 0.5

    return sentencePositionWeightMap
def integrateSentence(sentences, sentenceScoreMap,
                      sentenceArticleIntersectionMap,
                      sentencePositionWeighMap,
                      sentenceLengthMap,
                      sentenceCueWordLengthMap):
    finalScoreMap = dict()
    for sentence in sentences:
        cumulativeScore = 0
        cumulativeScore += sentenceScoreMap[sentence] * evalWeight_tfScores
        cumulativeScore += sentenceArticleIntersectionMap[sentence] * evalWeight_titleIntersection
        cumulativeScore += sentencePositionWeighMap[sentence] * evalWeight_sentencePosition
        cumulativeScore += sentenceLengthMap[sentence] * evalWeight_sentenceLength
        cumulativeScore += sentenceCueWordLengthMap[sentence] * evalWeight_sentenceCueWord
        finalScoreMap[sentence] = cumulativeScore
    maxSentenceCount = math.ceil(config['extractPercent'] * len(sentences))
    sortedTupleList = sorted(finalScoreMap.items(), key=lambda x:-x[1])[:maxSentenceCount]
    topWordDict = dict((x, y) for x, y in sortedTupleList)
    finalparagraph = ""
    for sentence in sentences:
        if sentence in topWordDict:
            finalparagraph += sentence + "."
    return finalparagraph

def writeSummaryToFile(filePath, text):
    fileHandler = open(filePath,"w")
    fileHandler.write(text)

traverserFolder(rootDir)
print(globalFileContent)
calculateInverseDocFrequencies()
generateSummary(rootDir)



