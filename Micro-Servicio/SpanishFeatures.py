
import datetime
import re
import json




class RelevantInformation():

    def __init__(self,whisper_model,spacy_model,audio,presentences,matcher,nlp,issue,requests,broker_format) -> None:
                
        self.nlp = nlp
        self.issue = issue
        self.audio = audio
        self.matcher = matcher
        self.requests = requests
        self.format = broker_format
        self.spacy_model= spacy_model
        self.presentences = presentences
        self.whisper_model= whisper_model
        self.sentence = self.audioToText(self.audio)

    def audioToText(self,audio):
        result = self.whisper_model.transcribe(audio)
        sentence = self.spacy_model(result["text"])
        return sentence

    def get_intention(self):

        intentions = []

        for presentence in self.presentences:
            intentions.append(self.sentence.similarity(presentence))
        intention = intentions.index(max(intentions))
        
        return intention,intentions[intention]
    
    def get_relevant_information(self):

        intention,percentage= self.get_intention()

        if percentage < 0.4:
            print(self.requests['fail'])

        else:
            self.clean_format()
            self.get_issue()
            matcher = self.matcher(self.sentence)
            self.format['raw'] = self.sentence.text
            self.get_current_hour()

            if intention >= 0 and intention <= 2:            
                self.format["action"] = self.requests['appointment']
                self.get_physician(matcher)
                self.get_date(matcher)
                self.get_time(matcher)

            elif intention >= 3 and intention <= 5:
                self.format['action'] = self.requests['reminder']
                self.get_date(matcher)
                self.get_time(matcher)
  
            elif intention >= 6:
                self.format['action'] = self.requests['search']
                self.get_information(matcher)
            
            self.format = json.dumps(self.format)
            
            return self.format

    def get_matches(self,patterns,matcher):

        matches = [match for match in matcher if self.nlp.vocab.strings[match[0]] in patterns]
        return matches
    
    def get_physician(self, matcher):

        physician_patterns = ['physician_pattern']
        matches = self.get_matches(physician_patterns[::],matcher)

        if len(matches) == 1:
            self.format["physician"] = self.sentence[matches[0][1]:matches[0][2]].text

        elif len(matches) > 1:
            index = len(matches)
            self.format["physician"] = self.sentence[matches[index-1][1]:matches[index-1][2]].text

    def get_date(self, matcher):


        date_patterns=["date_pattern1","date_pattern2","date_pattern3"]
        matches_pattern1 = self.get_matches(date_patterns[0],matcher)
        matches_pattern2 = self.get_matches(date_patterns[1],matcher)
        matches_pattern3 = self.get_matches(date_patterns[2],matcher)


        if len(matches_pattern1) == 1:
            self.format['date'] = self.sentence[matches_pattern1[0][1]:matches_pattern1[0][2]].text
        elif len(matches_pattern2) == 1 :
            self.format['date'] = self.sentence[matches_pattern2[0][1]:matches_pattern2[0][2]].text
        elif len(matches_pattern2)>1:
            index = len(matches_pattern2)
            self.format['date'] = self.sentence[matches_pattern2[index-1][1]:matches_pattern2[index-1][2]].text
        elif len(matches_pattern3)==1:
            self.format['date'] = self.sentence[matches_pattern3[0][2]-1].text

    def get_time(self,matcher):
        
        span = None
        expression = r"(?:1[012]|0?[1-9])(?:[.,][0-5]\d)"

        for match in re.finditer(expression,self.sentence.text):
            start,end = match.span()
            span = self.sentence.char_span(start,end)

        if span is not None:
            time = self.correct_time(span.text)
            time_patterns3 = ['time_pattern6']
            matches3 = self.get_matches(time_patterns3,matcher)

            if len(matches3) > 0:
                self.format['time'] = time + " "+self.sentence[matches3[0][1]:matches3[0][2]].text

            else:
                self.format['time'] = time
        else:
            time_patterns1 = ['time_pattern1','time_pattern3','time_pattern4']
            time_patterns2 = ['time_pattern5']    
            matches1 = self.get_matches(time_patterns1[::],matcher)

            if len(matches1) == 1:
                self.format['time'] = self.sentence[matches1[0][1]:matches1[0][2]].text

            elif len(matches1):
                index = len(matches1) 
                self.format['time'] = self.sentence[matches1[index-1][1]:matches1[index-1][2]].text

            else:
                matches2 = self.get_matches(time_patterns2,matcher)

                if len(matches2) > 0:
                    index = len(matches2)
                    time = self.sentence[matches2[index-1][1]+1:matches2[index-1][2]].text                  
                    self.format['time'] = time 

    def correct_time(self,time):
        numbers = ['1','2','3','4','5','6','7','8','9','0']
        punctuation = ['.',',']

        if time[1] in numbers:
            time = time[0:2] + ':' +time[3::]
            
        else:
            time = time[0] + ':' + time[2::]

        return time
    
    def get_information(self,matcher):
        search_patterns = ['search_pattern1','search_pattern2','search_pattern3','search_pattern4']
        matches1 = self.get_matches(search_patterns[0],matcher)
        matches2 = self.get_matches(search_patterns[1],matcher)
        matches3 = self.get_matches(search_patterns[2],matcher)
        matches4 = self.get_matches(search_patterns[3],matcher)

        if len(matches1) >0:

            if len(matches2)>0:

                if matches2[0][1] > matches1[0][1]:
                    self.format['search'] = self.sentence[matches2[0][1]::].text

            elif len(matches3)>0:

                if self.sentence[matches3[0][1]+1].lemma_ == 'el':
                    self.format['search'] = self.sentence[matches3[0][1]+2::].text

                else:
                    self.format['search'] = self.sentence[matches3[0][1]+1::].text

        elif len(matches2) > 0:
                self.format['search'] = self.sentence[matches2[0][1]::].text
                
        elif len(matches3) > 0:
            
            if self.sentence[matches3[0][1]+1].lemma_ == 'el':
                self.format['search'] = self.sentence[matches3[0][1]+2::].text
                
            else:
                self.format['search'] = self.sentence[matches3[0][1]+1::].text

        elif len(matches4)>0:
            self.format['serach'] = self.sentence[matches4[0][1]+1::].text
                

    def get_current_hour(self):

        current_hour = datetime.datetime.now().time()
        current_hour_str = current_hour.strftime("%H:%M:%S")
        self.format['timestamp'] = current_hour_str

    def get_issue(self):
        self.format['issue'] = str(self.issue)

    def clean_format(self):

        self.format['raw'] = ""
        self.format['action'] = ""
        self.format['search'] = ""
        self.format['place']= ""
        self.format['physician'] = ""
        self.format['date'] = ""
        self.format['time'] = ""
        self.format['timestamp'] = ""
        self.format['user-id'] = ""
        self.format['issue'] = ""












