import numpy as np
import sklearn
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
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
        start_words = ["start", "take", "write"]
        last_words = ["last", "previous", "just"]
        delete_words = ["delete"]
        number_words = ["number", "total", "many"]
        syn_start_words = []
        syn_last_words = []
        syn_delete_words = []
        syn_number_words= []
        for i in start_words:
            syns = wn.synsets(i)
            for j in syns:
                syn_start_words.append(syns[j].lemmas()[0].name())
        for i in last_words:
            syns = wn.synsets(i)
            for j in syns:
                syn_last_words.append(syns[j].lemmas()[0].name())
        for i in delete_words:
            syns = wn.synsets(i)
            for j in syns:
                syn_delete_words.append(syns[j].lemmas()[0].name())
        for i in number_words:
            syns = wn.synsets(i)
            for j in syns:
                syn_number_words.append(syns[j].lemmas()[0].name())
        self.start_words = syn_start_words
        self.last_words = syn_last_words
        self.delete_words = syn_delete_words
        self.number_words = syn_number_words

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

        start_response = "OK, what would you like me to say?"
        last_response = "Your last note was: "
        delete_response = "OK, I deleted your previous note."
        number_response = "You have x notes."

        for word in lem_sentence:
            if word in self.start_words:
                return start_response;
            if word in self.last_words:
                return last_response
            if word in self.delete_words:
                return delete_response
            if word in self.number_words:
                return number_response


        return "Sorry, I didn't understand that."
