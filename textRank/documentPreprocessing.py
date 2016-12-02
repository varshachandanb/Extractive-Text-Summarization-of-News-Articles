from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import re
import nltk

class document_Processing:

    def not_stopword(self,word):
        if word.lower() in nltk.corpus.stopwords.words('english'):
            return False
        else:
            return True

    def process(self,sentence, stopwords):
        word_list = []
        lemmatizer = WordNetLemmatizer()
        result = ""
        word_list = sentence.split()

        for words in word_list:
            words = lemmatizer.lemmatize(words)
            words = str(words).strip().lower()
            words = re.sub('[^A-Za-z]+', '', words)
            #if words not in stopwords:
            if (self.not_stopword(words)):
                result = result + " " + words

        return result.strip()

    def preprocessing(self,source_file,sentence_Filtered_File,stopwords_file):
        stopwords = {}
        document_text = ""

        #with open(stopwords_file, 'r',encoding="latin1") as f:
        #    for line in f:
        #        temp_line = line.strip()
        #        if temp_line not in stopwords:
        #            stopwords[temp_line] = 1

        heading = True
        with open(source_file, 'r',encoding="latin1") as f:
            for line in f:
                if heading:
                    heading = False
                    continue
                temp_line = line.strip()
                if (len(document_text) == 0):
                    document_text = temp_line
                else:
                    document_text = document_text + " " + temp_line

        sentences = sent_tokenize(document_text)
        #print(sentences)

        f = open(sentence_Filtered_File, 'w',encoding="latin1")
        for sentence in sentences:
            f.write(sentence + "#" + self.process(sentence, stopwords))
            f.write("\n")
        f.close()