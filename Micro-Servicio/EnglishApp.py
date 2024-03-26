from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from Folder import FolderFactory
from AudioFIle import AudioFile
from MainConfig import MainConfiguration as MC
from MainConfig import LanguageConfig as LC
from EnglishPatterns import EnglishConfig
import numpy as np
import wave
import time
import torch

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///token.db'  # Nombre de la base de datos
data_base = SQLAlchemy(app)


from EnglishFeatures import RelevantInformation

config = MC()
json_mconfig = config.getConfigFile()
whisper_model,spacy_model= config.loadConfig()
english = json_mconfig['CONFIG']['english']
json = LC(english)
json_lgconfig = json.getConfigFile()
english_config = EnglishConfig(spacy_model,json_lgconfig)
matcher = english_config.chargePatterns()
json.closeJson()


@app.route("/whisper", methods = ["POST"])
def translate():

    files= request.files.getlist("file")
    FolderFactory.build_folder("request")

    for file in files:
        audio = AudioFile().save_file(file,"request",True)

    #Model().use_model(audio)
     
    #t1 = time.time()
    torch.set_num_threads(4)

    result = whisper_model.transcribe(audio)
    message = result["text"]
    sentence = spacy_model(message.lower())
    intention = RelevantInformation(sentence,matcher,spacy_model,json_lgconfig)
    response = intention.get_intention() 
    data_base.create_all()

    #print("MESSAGE: ",message)

    #t2 = time.time()
    #tf = t2-t1
    
    #print ("Tiempo de traducción: ", tf, "segundos")
    
    return response

@app.route("/newUser", methods=["POST"])
def makeSpeechRecognizer():

    files= request.files.getlist("archivos")
    path = FolderFactory.build_folder("user")
    audio = AudioFile()
    audio.savefiles(files,path)
    audio.file_segmentation(path)

    return 'Audios Guardados'     

@app.route("/esp32", methods=["POST"])
def esp32Translate():
    
    torch.set_num_threads(4)
    time1 = time.time()
    audio_data = request.data
    audio_data_array = np.frombuffer(audio_data, dtype=np.int16)
    output_file = "received_audio.wav"

    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(1)  # 1 canal (mono)
        wf.setsampwidth(2)  # Tamaño de muestra en bytes (16 bits = 2 bytes)
        wf.setframerate(16000)  # Frecuencia de muestreo (ajusta según tus datos)
        wf.writeframes(audio_data_array.tobytes())    

    result = whisper_model.transcribe("received_audio.wav")    
    message = result["text"]
    time2 = time.time()
    print("Tiempo de procesamiento del mensaje: ", time2-time1)
    print("\n\n",message,"\n\n")


    patterns = json_lgconfig['PATTERNS']['pattern_names'][24]
    sentence = spacy_model(message.lower())
    matcher2 = matcher(sentence)
    matches = [match for match in matcher2 if spacy_model.vocab.strings[match[0]] in patterns]

    if(len(matches)>0):
        code = "200"    
    else:
        code = "220"
        
    return code

def create_tables():
    with app.app_context():
        data_base.create_all()

# Start the Server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)
