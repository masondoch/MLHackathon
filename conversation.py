import numpy as np
import sklearn
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet 
# first command: start, take, write 
# second command: storing a string 
# retrieve the last note: (going through the array where we stored the notes) last, was (??), previous, just (wrote)
# delete the last note: delete
# total number of notes: number, total, many, 

class Conversation:

    def __init__(self):
        '''
        The init function: Here, you should load any
        PyTorch models / word vectors / etc. that you
        have previously trained.
        '''
        self.size = 0
        pass

    def respond(self, sentence):
        '''
        This is the only method you are required to support
        for the Conversation class. This method should accept
        some input from the user, and return the output
        from the chatbot.
        '''
        wnl = WordNetLemmatizer()
        punct_array = [',', '.', '?', '!', '-', ';', ':']
        word_array = nltk.word_tokenize(sentence)
        filtered_word_array = [word for word in word_array if word not in punct_array]

        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in filtered_word_array if not word in stop_words]

        lem_sentence = [wnl.lemmatize(i) for i in filtered_sentence]

        return sentence
