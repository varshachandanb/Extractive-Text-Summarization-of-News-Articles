from .documentPreprocessing import document_Processing
from .pageRank import page_Rank

source_file = "InputFile.txt"
sentence_Filtered_File = "preprocessed_text.txt"
targetFile = "TargetFile1.txt"
stopwords_file = "stopwords.txt"
max = 3

doc = document_Processing()
doc.preprocessing(source_file,sentence_Filtered_File,stopwords_file)

pageScore = page_Rank()
pageScore.calculatePageRank(sentence_Filtered_File,targetFile,max)




