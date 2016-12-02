import math
class idf_cosine_similarity:

    def getDocumentArray(self, sentenceList):
        result = []
        for sentence in sentenceList:
            tempList = sentence.split()
            result.append(tempList)

        return result

    def getWordCounts(self, documentArray):
        result = []
        wordDict = {}
        for array in documentArray:
            tempDict = {}
            tempSet = set()
            for word in array:
                tempSet.add(word)
                if word in tempDict:
                    tempDict[word] += 1
                else:
                    tempDict[word] = 1

            for elem in tempSet:
                if elem in wordDict:
                    wordDict[elem] += 1
                else:
                    wordDict[elem] = 1

            result.append(tempDict)

        return (result, wordDict)

    def getIdfValues(self, no_of_nodes, idfWordCount):
        result = {}
        for word in idfWordCount:
            result[word] = math.log10(no_of_nodes/idfWordCount[word])
        return result

    def calculateIDFCosineSimilarity(self, dictA, dictB, idfDict):
        wordSet = dictA.keys() & dictB.keys()
        setA = set(dictA)
        setB = set(dictB)
        if (len(setA.intersection(setB)) == 0):
            return 0
        scoreAB = 0.000
        scoreA = 0.000
        scoreB = 0.000
        for word in wordSet:
            frequencyA = dictA[word]
            frequencyB = dictB[word]
            idfWord = idfDict[word]

            scoreAB = scoreAB + (frequencyA * frequencyB * idfWord ** 2)

        for word in dictA:
            idfWord = idfDict[word]
            frequencyA = dictA[word]
            scoreA = scoreA + (frequencyA ** 2 * idfWord ** 2)

        for word in dictB:
            idfWord = idfDict[word]
            frequencyB = dictB[word]
            scoreB = scoreB + (frequencyB ** 2 * idfWord ** 2)

        score = (scoreAB / (math.sqrt(scoreA) * math.sqrt(scoreB)));

        return score