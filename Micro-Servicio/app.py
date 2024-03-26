import wave
import numpy as np
from AudioFile import AudioFile
from flask import Flask, request
from Repository import RespositoryFactory
from flask_sqlalchemy import SQLAlchemy
from MainConfig import MainConfiguration as MC
from MainConfig import Language as LC
from Kafka import BrokerCommunication as Broker
from Model import Model



#--------------------------------------------------------------#
#          Initialice Database for robot token                 #
#--------------------------------------------------------------#
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///token.db'
data_base = SQLAlchemy(app)

config = MC()
json_mconfig = config.getConfigFile()
whisper_model,spacy_model= config.loadConfig()


if config.getLanguage() == 1:
    from SpanishPatterns import SpanishConfig
    from SpanishFeatures import RelevantInformation


    spanish = json_mconfig['CONFIG']['spanish']
    broker_info = json_mconfig['KAFKA']
    config.closeJson() 

    json = LC(spanish)
    json_lgconfig = json.getConfigFile()
    sentences = json_lgconfig['SENTENCES']
    features = json_lgconfig['FEATURES']
    requests = features['REQUEST']
    broker_format = json_lgconfig['BROKERFORMAT']

    spanish_config = SpanishConfig(spacy_model,sentences,features)
    sentences, matcher = spanish_config.loadConfiguration()
    json.closeJson()

else: 
    from EnglishPatterns import EnglishConfig
    from EnglishFeatures import RelevantInformation

    english = json_mconfig['CONFIG']['english']
    json = LC(english)
    json_lgconfig = json.getConfigFile()
    english_config = EnglishConfig(spacy_model,json_lgconfig)
    matcher = english_config.chargePatterns()
    json.closeJson()


issue = 0

app = Flask(__name__)




@app.route("/whisper", methods = ["POST"])
def translate():

    files= request.files.getlist("file")
    RespositoryFactory.build_repository("request")

    for file in files:
        audio = AudioFile().saveFile(file,"request",True)
    
    if config.getLanguage() == 1:
        
        #user = Model().use_model(audio)
        
        #if not user:
        #    return "Usuario no identificado"
        #else:
            intention = RelevantInformation(whisper_model,spacy_model,audio,sentences,matcher,spacy_model,issue,requests,broker_format)
            formato = intention.get_relevant_information()
            return "ok"
    
    else:
        intention = RelevantInformation(whisper_model,spacy_model,audio,matcher,spacy_model,json_lgconfig)
        response = intention.get_intention()
        data_base.create_all()
        return response


@app.route("/newUser", methods=["POST"])
def makeSpeechRecognizer():

    files= request.files.getlist("archivos")
    path = RespositoryFactory.build_repository("user")
    audio = AudioFile()
    audio.saveFiles(files,path)
    audio.fileSegmentation(path)

    return 'Audios Guardados'


#------------------------------------------------------------#
#              Command detection using Esp32                 #
#------------------------------------------------------------#
@app.route("/esp32", methods=["POST"])
def esp32Translate():

    audio_data = request.data
    audio_data_array = np.frombuffer(audio_data, dtype=np.int16)
    output_file = json_mconfig["AUDIO"]["request"]
    AudioFile().createWavFile(audio_data_array,output_file)    
    audio = json_mconfig["AUDIO"]["request"]

    if config.getLanguage() == 1:
        intention = RelevantInformation(whisper_model,spacy_model,audio,sentences,matcher,spacy_model,issue,requests,broker_format)
        formato = intention.get_relevant_information()
        #Broker().Producer(formato)
        return "ok"
    else:
        intention = RelevantInformation(whisper_model,spacy_model,audio,matcher,spacy_model,json_lgconfig)
        response = intention.get_intention()
        data_base.create_all()
        return response
        
#------------------------------------------------------------#
#                        WakeWord detection                  #
#------------------------------------------------------------#
@app.route("/wakeword", methods=["POST"])
def esp32Wakeword():
    
    audio_data = request.data
    audio_data_array = np.frombuffer(audio_data, dtype=np.int16)
    output_file = json_mconfig["AUDIO"]["wakeword"]
    AudioFile().createWavFile(audio_data_array,output_file)
    result = whisper_model.transcribe(json_mconfig["AUDIO"]["wakeword"])
    message = result["text"]
    patterns = json_lgconfig['PATTERNS']['pattern_names'][24]
    sentence = spacy_model(message.lower())
    matcher2 = matcher(sentence)
    matches = [match for match in matcher2 if spacy_model.vocab.strings[match[0]] in patterns]

    if matches:
        return "OK"
    else:
        return "NOT"

#------------------------------------------------------------------#
#                      Create DataBase Table                       #
#------------------------------------------------------------------#
def create_tables():
    with app.app_context():
        data_base.create_all()

# Start the Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)
