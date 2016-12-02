from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
import re

class document_Processing:

    def process(self,sentence, stopwords):
        word_list = []
        lemmatizer = WordNetLemmatizer()
        result = ""
        word_list = sentence.split()

        for words in word_list:
            words = lemmatizer.lemmatize(words)
            words = str(words).strip().lower()
            if words not in stopwords:
                if re.match('[a-z]+', words) or re.match('[0-9]+', words) or re.match('[a-z]+[0-9]+',
                                                                                      words) or re.match('[0-9]+[a-z]+',
                                                                                                         words):
                    result = result + " " + words

        return result.strip()

    def preprocessing(self,source_file,sentence_Filtered_File,stopwords_file):
        stopwords = {}
        document_text = ""

        with open(stopwords_file, 'r') as f:
            for line in f:
                temp_line = line.strip()
                if temp_line not in stopwords:
                    stopwords[temp_line] = 1

        with open(source_file, 'r') as f:
            for line in f:
                temp_line = line.strip()
                if (len(document_text) == 0):
                    document_text = temp_line
                else:
                    document_text = document_text + " " + temp_line

        sentences = sent_tokenize(document_text)
        print(sentences)

        f = open(sentence_Filtered_File, 'w')
        for sentence in sentences:
            f.write(sentence + "#" + self.process(sentence, stopwords))
            f.write("\n")
        f.close()