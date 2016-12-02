import networkx as nx
import operator
from cosineSimilarity import cosine_similarity
import json
import math

config = {}
data = ""

with open('../config.json') as data_file:
    data = json.load(data_file)
config =data

class page_Rank:

    def outputToTarget(self,combined,PR_score,target_File,max):
        text_score_dict = {}

        for x in range (len(combined)):
            text_score_dict[combined[x]] = PR_score[x]

        sorted_text = []
        sorted_text = sorted(text_score_dict.items(), key=operator.itemgetter(1),reverse=True)
        #print("Sorted according to page rank\n")
        #print(sorted_text)

        maxSentenceCount = math.ceil(config['extractPercent'] * len(sorted_text))

        print (target_File)
        f = open(target_File, 'w',encoding="latin1")
        count = 0
        for key,val in sorted_text:
            sent = key.strip().split("#")
            f.write(sent[0])
            count += 1
            if count == maxSentenceCount:
                break
        f.close()



    def calculatePageRank(self,sentence_Filtered_File,target_File,max):
        combined = []
        clean = []

        with open(sentence_Filtered_File, 'r',encoding="latin1") as f:
            for line in f:
                temp = line.strip().split("#")
                if(len(temp) == 2):
                    combined.append(line.strip())
                    clean.append(temp[1])

        #print (clean)
        #print ("\n")
        #print (combined)
        no_of_nodes = len(clean)

        cosine = cosine_similarity()
        G = nx.DiGraph()

        for i in range(no_of_nodes):
            for j in range(no_of_nodes):
                if i != j:
                    w = cosine.calculateCosineSimilarity(clean[i],clean[j])
                    if w > 0:
                        G.add_edge(i,j,weight=w)
                        G.add_edge(j,i,weight=w)

        pr = nx.pagerank(G, alpha=0.85, max_iter=100)
        PR_score = []

        for i in range(no_of_nodes):
            if i in pr:
                PR_score.append(pr[i])
            else:
                PR_score.append(0)


        #print (pr)
        #print (PR_score)
        self.outputToTarget(combined,PR_score,target_File,max)



