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
        start_words = ["start", "take", "write", "make", "remind"]
        last_words = ["last", "previous", "just"]
        delete_words = ["delete"]
        number_words = ["number", "total", "many"]
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
        index_array = [ordinal(n) for n in range(1, 20)]
        syn_start_words = []
        syn_start_words.extend(start_words)
        syn_last_words = []
        syn_last_words.extend(last_words)
        syn_delete_words = []
        syn_delete_words.extend(delete_words)
        syn_number_words= []
        syn_number_words.extend(number_words)
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
        self.start = False
        self.delete = False
        self.last = False
        self.number = False
        self.index = False
        self.track ={}
        self.message_array = []
        self.message = ""
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
        filtered_sentence = [w for w in filtered_word_array if not w in stop_words]

        lem_sentence = [wnl.lemmatize(i) for i in filtered_sentence]
        print(lem_sentence)
        if self.start:
            print(sentence)
            self.notes.append(sentence)
            self.start = False
            for i in range(len(lem_sentence)): 
                self.track[lem_sentence[i]]= self.size
            return "Note saved."
        

        start_response = "OK, what would you like me to say?"
        last_response = "Your last note was: "
        delete_response = "OK, I deleted your previous note."
        number_response = "You have "
        index_response = "Here is that note: "
        default_response = "Sorry, I didn't understand that."
        for word in lem_sentence:
            print(word)
            if word in self.start_words:

                self.size += 1
                self.start = True
                self.message_array = [i for i in lem_sentence if i not in start_words and i != "note"]
                for i in self.message_array: 
                    self.message += i + " "
                if self.message == "" : 
                    return start_response
                else: 
                    self.notes.append(self.message)
                    self.message = ""
                    self.start = False
                    return "Note saved"
                #return start_response

            if word in self.last_words:
                if self.size == 0:
                    return "You don't have any notes currently."
                self.last = True
                if not self.delete: 
                    self.last = False
                    return last_response + self.notes[self.size - 1]
                else: 
                    self.size -= 1
                    self.delete = False
                    self.last = False
                    return delete_response
            if word in self.delete_words:
                #self.notes.pop()
                self.delete = True
                #self.size -= 1
                #return delete_response
            if word in self.number_words:
                if self.size == 1:
                    return number_response + str(1) + " note."
                return number_response + str(self.size) + " notes."
            if word in self.index_words:
                if not self.delete: 
                    if self.size - 1 < int(word[0]) - 1:
                        return "Sorry, you don't have that many notes."
                    return index_response + self.notes[int(word[0]) - 1]
                else: 
                    if self.last: 
                        self.notes.pop()
                        self.last = False
                        self.delete = False
                        self.size-=1
                        return delete_response
                    else : 
                        self.notes.pop(int(word[0]) - 1)
                        self.delete = False
                        self.size-=1
                        return "OK I deleted your " + str(word) + " note."
            if word in self.track.keys(): 
                value = self.track[word] - 1
                return "Your notes was: " + self.notes[value]    
        return default_response