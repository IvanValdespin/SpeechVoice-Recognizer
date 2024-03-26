from openvino.runtime import Core
import WhisperOpenVino as wov
from functools import partial
import whisper
import spacy
import json


class MainConfiguration():

    def __init__(self) -> None:

        self.json_path = "MainConfig.json"
        self.config,self.file = self.readConfig(self.json_path)
        self.language = self.chooseLanguage()

    def readConfig(self,json_path:str)-> json:
        try:
            #Reading configuration file 
            with open(json_path,'r') as config:
                json_config = json.load(config)
            return json_config, config
        except Exception as e:
            print(e)

    def closeJson(self):
        self.file.close()
    
    def getConfigFile(self)->json:
        return self.config
    
    def getLanguage(self):
        return self.language
    
    def chooseLanguage(self):
        
        language_message = self.config['LANGUAGE']['message']
        language = int(input(language_message))
        return language

    def loadWhisper(self):

        #Initialice OpenVino module
        core = Core()
        #Get whisper data configuration
        whisper_data = self.config['WHISPER']
        
        try:
            
            #Load whisper model 
            model = whisper.load_model(whisper_data['whisper_model'], 
                                       device = whisper_data['device'])
            #Delete original whisper decoder and encoder modules
            del model.decoder
            del model.encoder

            #Charge new encoder and decoder modules 
            model.encoder = wov.OpenVINOAudioEncoder(core,whisper_data['NEW_CONFIG']['encoder'])
            model.decoder = wov.OpenVINOTextDecoder(core, whisper_data['NEW_CONFIG']['decoder'])
            model.decode = partial(wov.decode, model)
            model.parameters = wov.parameters
            model.logits = partial(wov.logits, model)

            return model
        
        except Exception as e:
            print(e)

    def loadSpacy(self) -> None:

        spacy_data = self.config['SPACY']

        try:
            if self.language == 1:
                spacy_model = spacy.load(spacy_data['MODELS']['spanish'])
                return spacy_model
            else: 
                spacy_model = spacy.load(spacy_data['MODELS']['english'])
                return spacy_model
            
        except Exception as e:
            print(e)
    
    def loadConfig(self):
        whisper_model = self.loadWhisper()
        spacy_model = self.loadSpacy()

        return whisper_model, spacy_model
    
    

class Language():

    def __init__(self,json1) -> None:
        self.json = json1
        self.config, self.file = self.loadJson()

    def loadJson(self)->json:
        
        try:
            #Reading configuration file 
            with open(self.json,'r') as config:
                json_config = json.load(config)
            return json_config, config
        except Exception as e:
            print(e)

    def getConfigFile(self)->json:
        return self.config

    def closeJson(self)->None:
        self.file.close()
        



