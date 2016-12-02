import networkx as nx
import operator
from LexRank.IDFCosineSimilarity import idf_cosine_similarity
import numpy
import math
class lexRank:

    def outputToTarget(self,inputText,target_File,max):
        outputFile = open(target_File, 'w')
        for i in range(max):
            outputFile.write(inputText[i])
            outputFile.write("\n")
        outputFile.close()

    def calculateLexRank(self,sentence_Filtered_File,target_File, percentage, initialText):
        combined = []
        clean = []

        with open(sentence_Filtered_File, 'r') as f:
            for line in f:
                temp = line.strip().split("#")
                combined.append(line.strip())
                clean.append(temp[1])


        no_of_nodes = len(clean)
        max = math.ceil(percentage * no_of_nodes)
        idfCosine = idf_cosine_similarity()

        documentArray = idfCosine.getDocumentArray(clean)
        (documentWordCounts, idfWordCount) = idfCosine.getWordCounts(documentArray)
        idfValues = idfCosine.getIdfValues(no_of_nodes, idfWordCount)

        cosineMatrix = numpy.zeros((no_of_nodes, no_of_nodes))
        degree = numpy.zeros(no_of_nodes)
        threshold = 0.1


        for i in range(no_of_nodes):
            for j in range(no_of_nodes):
                cosineValue = idfCosine.calculateIDFCosineSimilarity(documentWordCounts[i], documentWordCounts[j], idfValues)
                if(cosineValue > threshold):
                    cosineMatrix[i][j] = 1
                    degree[i] += 1
                else:
                    cosineMatrix[i][j] = 0

        for i in range(no_of_nodes):
            for j in range(no_of_nodes):
                cosineMatrix[i][j] = cosineMatrix[i][j]/degree[i]

        tempResult = (powerMethod(cosineMatrix, no_of_nodes, 0.001)).T.tolist()[0]

        initialText.sort(key=dict(zip(initialText, tempResult)).get)
        self.outputToTarget(initialText, target_File, max)



def powerMethod(cosineMatrix, n, errorValue):
    pVector = numpy.full((n, 1), 1/n)
    delta = 1.0000
    tMatrix = cosineMatrix.T
    while(delta > errorValue):
        pNew = tMatrix.dot(pVector)
        diff = pNew - pVector
        delta = numpy.linalg.norm(diff)
        pVector = pNew

    return pVector