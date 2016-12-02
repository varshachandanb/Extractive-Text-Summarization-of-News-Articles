import math
class cosine_similarity:

    def calculateCosineSimilarity(self,A,B):
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

            AB = AB + (A_freq * B_freq)
            A_sq = A_sq + (A_freq * A_freq)
            B_sq = B_sq + (B_freq * B_freq)

        if (math.sqrt(A_sq) == 0 or math.sqrt(B_sq) == 0):
            return 0

        score = ((AB) / (math.sqrt(A_sq) * math.sqrt(B_sq)));
        return score




