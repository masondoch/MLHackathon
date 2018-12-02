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
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
        index_array = [ordinal(n) for n in range(1, 20)]
        syn_start_words = []
        syn_last_words = []
        syn_delete_words = []
        syn_number_words= []
        syn_index_words = []
        for i in start_words:
            syns = wn.synsets(i)
            for j in range(len(syns)):
                syn_start_words.append(syns[j].lemmas()[0].name())
        for i in last_words:
            syns = wn.synsets(i)
            for j in range(len(syns)):
                syn_last_words.append(syns[j].lemmas()[0].name())
        for i in delete_words:
            syns = wn.synsets(i)
            for j in range(len(syns)):
                syn_delete_words.append(syns[j].lemmas()[0].name())
        for i in number_words:
            syns = wn.synsets(i)
            for j in range(len(syns)):
                syn_number_words.append(syns[j].lemmas()[0].name())
        self.start_words = syn_start_words
        self.last_words = syn_last_words
        self.delete_words = syn_delete_words
        self.number_words = syn_number_words
        self.index_words = index_array
        self.notes = []
        self.in_progress = False
        pass

    def respond(self, sentence):
        '''
        This is the only method you are required to support
        for the Conversation class. This method should accept
        some input from the user, and return the output
        from the chatbot.
        '''
        if self.in_progress:
            self.notes.append(sentence)
            self.in_progress = False
            return "Note saved."
        wnl = WordNetLemmatizer()
        punct_array = [',', '.', '?', '!', '-', ';', ':']
        word_array = nltk.word_tokenize(sentence)
        filtered_word_array = [word for word in word_array if word not in punct_array]

        stop_words = set(stopwords.words('english'))
        filtered_sentence = [w for w in filtered_word_array if not w in stop_words]

        lem_sentence = [wnl.lemmatize(i) for i in filtered_sentence]

        start_response = "OK, what would you like me to say?"
        last_response = "Your last note was: "
        delete_response = "OK, I deleted your previous note."
        number_response = "You have "
        index_response = "Here is that note: "

        for word in lem_sentence:
            if word in self.start_words:
                self.size += 1
                self.in_progress = True
                return start_response;
            if word in self.last_words:
                if self.size == 0:
                    return "You don't have any notes currently."
                return last_response + self.notes[self.size - 1]
            if word in self.delete_words:
                self.notes.pop()
                self.size -= 1
                return delete_response
            if word in self.number_words:
                if self.size == 1:
                    return number_response + str(1) + " note."
                return number_response + str(self.size) + " notes."
            if word in self.index_words:
                return index_response + self.notes[int(word[0]) - 1]


        return "Sorry, I didn't understand that."
