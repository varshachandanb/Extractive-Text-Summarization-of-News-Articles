
## Authors :

Deepthi Girish Singapura <br/>
Varsha Chandan Bellara <br/>
Srushti Singatagere Basavaraj <br/>
Shiva Shankar Bidadi Nanjundaswamy <br/>




## Project Name

Title : Extractive Text Summarization with Lexical Chain, Modified Text Rank, Text Rank and TConspectus for news articles.
<br/>

## Data Set:
Raw Data Sets to be Downloaded from : http://mlg.ucd.ie/datasets/bbc.html
<br/>
## PreProcessing

Article Tokenization<br/>
Case folding of token <br/>
Stop word removal <br/> 
Lemmatization, Remove non alpha-numeric characters

## Usage
LexRank: 
python3 main.py 
<br />
PageRank:
python3 main.py 
<br />
Lexical Chain:
python3 main.py 
<br />
Hybrid:
python3 summarizer.py
<br />
Sumy:
python3 extractSummary.py
<br />
Evaluate Summaries: 
python3 documentComparator.py

## Algorithm Evaluation:
Generated summaries based on compression ratio <br/>
Expressed documents as vectors<br/>
Compared all the Algo-generated-summaries using cosine values<br/>

## Accuracy:
## 10% 
LexRank : 52.57 % <br/>
Pagerank : 51.18 % <br/>
Lexical Chain: 74.36 % <br/>
Hybrid Algorithm : 61.45 % <br/>

## 20% 
LexRank : 63.12 % <br/>
Pagerank : 61.91 % <br/>
Lexical Chain: 79.95 % <br/>
Hybrid Algorithm : 70.86 % <br/>

## 30% 
LexRank : 72.31 % <br/>
Pagerank : 71.11 % <br/>
Lexical Chain: 84.21 % <br/>
Hybrid Algorithm : 77.91 % <br/>

## 40% 
LexRank : 78.59 % <br/>
Pagerank : 78.13 % <br/>
Lexical Chain: 86.64 % <br/>
Hybrid Algorithm : 83.87 % <br/>






