
"""Created by Ivan Valdespin Garcia
    Date: June 23th 2023 at Science Computer Department of the University of St.Gallen"""

from spacy.matcher import Matcher
from Interfaces import IPatterns


class SpanishConfig(IPatterns):

    def __init__(self,nlp,spanish_sentences,features) -> None:
        self.nlp = nlp
        self.features = features
        self.matcher = Matcher(self.nlp.vocab)
        self.spanish_sentences = spanish_sentences

    def chargeSentences(self):
        
        procesed_sentences = []

        #Sentences for booking an appointment
        appointment_sentence1 = self.spanish_sentences['APPOINTMENT']['appointment1']
        appointment_sentence2 = self.spanish_sentences['APPOINTMENT']['appointment2']
        appointment_sentence3 = self.spanish_sentences['APPOINTMENT']['appointment3']
        #Sentences for taking medicine reminders
        reminder_sentence1 = self.spanish_sentences['REMINDERS']['reminder1']
        reminder_sentence2 = self.spanish_sentences['REMINDERS']['reminder2']
        reminder_sentence3 = self.spanish_sentences['REMINDERS']['reminder3']
        #Sentences for searching information about hoe to take medicine or topics about diabetes
        search_sentence1 = self.spanish_sentences['SEARCH']['search1']
        search_sentence2 = self.spanish_sentences['SEARCH']['search2']
        search_sentence3 = self.spanish_sentences['SEARCH']['search3']
        search_sentence4 = self.spanish_sentences['SEARCH']['search4']

        sentences = [appointment_sentence1, appointment_sentence2,appointment_sentence3,
                     reminder_sentence1,reminder_sentence2, reminder_sentence3,
                     search_sentence1,search_sentence2,search_sentence3,search_sentence4]
        
        for sentence in sentences:
            procesed_sentences.append(self.nlp(sentence))
        return procesed_sentences

    
    def createPatterns(self):

        #Patterns for finding the physician in the sentences
        physician_pattern = [{'LOWER':{'FUZZY1':{'IN':self.features['PHYSICIAN']}},'OP':'+'},{'POS':'PROPN','OP':'?'}]

        #Patterns for finding dates
        date_pattern1 = [{'POS':'NUM'},{'POS':'ADP'},{'POS':'NOUN'}] #DIA de MES
        date_pattern2 = [{'LOWER':{'FUZZY1':{'IN':self.features['DAYS']}},'OP':'?'}]
        date_pattern3 = [{'LOWER':'la','OP':'!'},{'LOWER':'mañana','OP':'+'}]
        
        #Patterns for finding time in an appointment

        time_pattern1 = [{"POS":"NUM",'OP':'+'},{"POS":"CCONJ",'OP':'+'},
                         {"LOWER":{'FUZZY1':{'IN':self.features['TIME_EXPRESSION']}},'OP':'+'},
                         {'LOWER':'de','OP':'?'},{'LOWER':'la','OP':'?'},
                         {'LOWER':{'FUZZY1':{'IN':self.features['TIME']}},'OP':'?'}]  #numero y media/cuarto (Opcionl : de la mañana, tarde, noche)
                
        time_pattern2 = [{'LOWER':'en','OP':'+'},{'LOWER':'la','OP':'+'},{"IS_DIGIT":True,'OP':'!'},
                         {'LOWER':{'FUZZY1':{'IN':self.features['TIME']}},'OP':'?'}] #en la (opcional: mañana, tarde, noche)
        
        time_pattern3 = [{'pos':'ADV','LOWER':'temprano','OP':'?'}] #temprano

        time_pattern4 = [{'POS':'ADP','OP':'?'},{'POS':'DET','OP':'+'},{'POS':'NUM','OP':'+'},
                         {"LOWER":'de','OP':'?'},{'LOWER':'la','OP':'?'},
                         {'LOWER':{'FUZZY1':{'IN':self.features['TIME']}},'OP':'?'}] #opcional(a) las numero:numero (opcional: de la mañana, tarde, noche)
        
        time_pattern5 = [{'LOWER':'de','OP':'+'},{'LOWER':'la','OP':'+'},{"IS_DIGIT":True,'OP':'!'},
                         {'LOWER':{'FUZZY1':{'IN':self.features['TIME']}},'OP':'?'}] #de la (opcional : mañana, tarde, noche)
        

        search_pattern1 = [{'LEMMA':'buscar','OP':'+'},{'LOWER':'información','OP':'?'},{'LOWER':'informacion','OP':'?'}]
        search_pattern2= [{'LOWER':'como','OP':'?'},{'LOWER':'cómo','OP':'?'}]
        search_pattern3 = [{'LOWER':'sobre','OP':'+'},{'LOWER':'acerca','OP':'?'}]
        search_pattern4 = [{'LOWER':'buscame'}]

        wake_word = [{"LOWER":{"FUZZY1":{"IN":["hello"]}},'OP':'+'}]

        patterns = [physician_pattern,
                    date_pattern1,date_pattern2,date_pattern3,
                    time_pattern1,time_pattern2,time_pattern3,time_pattern4,time_pattern5,
                    search_pattern1,search_pattern2,search_pattern3,search_pattern4,
                    wake_word]
        
        return patterns

        
    def chargePatterns(self):

        patterns = self.createPatterns()

        pattern_names = self.features['PATTERNS']
        counter = 0        
        
        for name in pattern_names:
            self.matcher.add(name,[patterns[counter]])
            counter += 1

        return self.matcher

    def loadConfiguration(self):
        sentences = self.chargeSentences()
        matcher = self.chargePatterns()

        return sentences, matcher


