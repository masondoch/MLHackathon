import numpy as np
import sklearn
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class Conversation:

    def __init__(self):
        '''
        The init function: Here, you should load any
        PyTorch models / word vectors / etc. that you
        have previously trained.
        '''
        pass

    def respond(self, sentence):
        '''
        This is the only method you are required to support
        for the Conversation class. This method should accept
        some input from the user, and return the output
        from the chatbot.
        '''
        punct_array = [',', '.', '?', '!', '-', ';', ':']
        word_array = nltk.word_tokenize(sentence)
        filtered_word_array = [word for word in word_array if word not in punct_array]

        return sentence
