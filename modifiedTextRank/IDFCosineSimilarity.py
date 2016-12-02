import math
class idf_cosine_similarity:

    def calculateWordCount(selfself, nodes):
        wordDict = {}
        for sentence in nodes:
            wordList = sentence.split()
            for word in wordList:
                if word in wordDict:
                    wordDict[word] += 1
                else:
                    wordDict[word] = 1

        return wordDict



    def calculateIDFCosineSimilarity(self,A,B, wordDict, sentenceCount):
        listA = A.split()
        listB = B.split()
        dictA = {}
        dictB = {}
        word_set = set()

        for word in listA:
            if word in dictA:
                dictA[word] += 1
            else:
                dictA[word] = 1
            word_set.add(word)

        for word in listB:
            if word in dictB:
                dictB[word] += 1
            else:
                dictB[word] = 1
            word_set.add(word)

        AB = 0.0000000
        A_sq = 0.0000000
        B_sq = 0.0000000

        for word in word_set:
            A_freq = 0
            B_freq = 0
            if word in dictA:
                A_freq = dictA[word]
            if word in dictB:
                B_freq = dictB[word]

            idfValue = calculateIDFValue(word, sentenceCount, wordDict)

            AB = AB + (A_freq * B_freq * idfValue * idfValue)
            A_sq = A_sq + (A_freq * A_freq * idfValue * idfValue)
            B_sq = B_sq + (B_freq * B_freq * idfValue * idfValue)

        score = ((AB) / (math.sqrt(A_sq) * math.sqrt(B_sq)));
        return score


def calculateIDFValue(word, sentenceCount, wordDict):
    idfValue = 0.000
    if word in wordDict:
        idfValue = math.log(sentenceCount/wordDict[word])
    idfValue = idfValue + 1
    return idfValue