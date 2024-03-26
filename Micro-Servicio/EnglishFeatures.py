
import json
import requests
from IoTCommunication import IoTCommunication
from Objects import Lamp, Blind, Robot
from MainConfig import LanguageConfig as LC
from EnglishPatterns import EnglishConfig
from MainConfig import MainConfiguration as MC



class RelevantInformation():

    def __init__(self,whisper_model,spacy_model,audio,matcher,nlp,json_lgconfig) -> None:

        self.nlp = nlp
        self.audio = audio
        self.matcher = matcher
        self.spacy_model= spacy_model
        self.whisper_model= whisper_model
        self.urls = json_lgconfig['URLS']
        self.actions = json_lgconfig['OBJECTS']
        self.sentence = self.audioToText(self.audio)
        self.instructuions = json_lgconfig['INSTRUCTIONS']
        self.patterns = json_lgconfig['PATTERNS']['pattern_names']
        

    def audioToText(self,audio):
        result = self.whisper_model.transcribe(audio)
        sentence = self.spacy_model(result["text"])
        return self.nlp(sentence)

    def get_intention(self):

        matcher = self.matcher(self.sentence)

        lamp_pat = self.get_matches(self.patterns[0],matcher)
        blinds_pat = self.get_matches(self.patterns[7],matcher)
        robot_pat = self.get_matches(self.patterns[11],matcher)


        if lamp_pat or blinds_pat or robot_pat:
            request = IoTCommunication()

            if lamp_pat:

                url = self.urls['lamp']
                status = request.sendGetStatus(url)
                status = json.loads(status.text)
                lamp_ins = self.instructuions['lamp']
                lamp_actions = self.actions['LAMP']['actions']
                lamp_properties = self.actions['LAMP']['properties']

                lamp = Lamp(status,self.nlp,self.sentence,self.patterns,matcher,lamp_ins,lamp_actions,lamp_properties)
                inst = lamp.getInstructions()
                response = request.sendPut2(url,inst)
                return str(response.status_code)
                
            elif blinds_pat:

                blinds_ins = self.instructuions['blinds']
                url = self.urls['blinds']
                blind_actions = self.actions['BLINDS']['actions']
                blind_properties = self.actions['BLINDS']['properties']

                blind = Blind(self.nlp,self.sentence,self.patterns,matcher,blinds_ins,blind_actions,blind_properties)
                inst = blind.getUpDown()
                response = request.sendPut2(url,inst)
                return response
            
            elif robot_pat:
                robot_ins = self.instructuions['robot']
                urls = self.urls['robot']
                robot_actions = self.actions['ROBOT']

                robot = Robot(self.nlp,matcher,urls, self.sentence,robot_actions,robot_ins,request,self.patterns)
                response = robot.getIntention()
                return response

        else:
            return self.actions['ROBOT']['messages']['fail']

            
    
    def get_matches(self,patterns,matcher):

        matches = [match for match in matcher if self.nlp.vocab.strings[match[0]] in patterns]
        return matches

