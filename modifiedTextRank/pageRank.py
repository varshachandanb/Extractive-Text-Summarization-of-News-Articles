import networkx as nx
import operator
from IDFCosineSimilarity import idf_cosine_similarity

class page_Rank:

    def outputToTarget(self,combined,PR_score,target_File,max):
        text_score_dict = {}

        for x in range (len(combined)):
            text_score_dict[combined[x]] = PR_score[x]

        sorted_text = []
        sorted_text = sorted(text_score_dict.items(), key=operator.itemgetter(1),reverse=True)
        print("Sorted according to page rank\n")
        print(sorted_text)

        f = open(target_File, 'w')
        count = 0
        for key,val in sorted_text:
            sent = key.strip().split("#")
            f.write(sent[0])
            f.write("\n")
            count += 1
            if count == max:
                break
        f.close()



    def calculatePageRank(self,sentence_Filtered_File,target_File,max):
        combined = []
        clean = []

        with open(sentence_Filtered_File, 'r') as f:
            for line in f:
                temp = line.strip().split("#")
                if(len(temp) == 2):
                    combined.append(line.strip())
                    clean.append(temp[1])


        no_of_nodes = len(clean)
        idfCosine = idf_cosine_similarity()
        G = nx.DiGraph()

        wordCount = idfCosine.calculateWordCount(clean)

        for i in range(no_of_nodes):
            for j in range(no_of_nodes):
                if i != j:
                    w = idfCosine.calculateIDFCosineSimilarity(clean[i],clean[j], wordCount, no_of_nodes)
                    G.add_edge(i,j,weight=w)
                    G.add_edge(j,i,weight=w)

        pr = nx.pagerank(G, alpha=0.85, max_iter=30)

        PR_score = []
        for key in pr:
            PR_score.append(pr[key])

        self.outputToTarget(combined,PR_score,target_File,max)